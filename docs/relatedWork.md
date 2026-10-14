# Reading List: MCP Documentation and Security

The summaries below explain each source's main focus and relevant security ideas. 

---

## 1. [MCP Official Documentation — Architecture, Specification, and Security Best Practices](https://modelcontextprotocol.io/)  

### Summary

The official MCP documentation is the primary reference for understanding what MCP is designed to do and how clients and servers are expected to communicate. MCP standardises how an AI application can discover and use external capabilities, such as tools, resources, and prompts.

The documentation describes the protocol's main components and interaction patterns. A host application typically contains or coordinates an MCP client, which connects to one or more MCP servers. Servers expose capabilities such as:

- **Tools:** callable functions that can perform actions or retrieve information, such as querying a service or reading a file.
- **Resources:** data or context that a client can retrieve and provide to a model.
- **Prompts:** reusable prompt templates or instructions exposed by a server.
- **Sampling:** a server-initiated request for the client to use its model to generate a completion. This is important from a security perspective because it introduces a route through which server-provided content can influence model behaviour.

MCP uses structured JSON-RPC messages and defined lifecycle and capability-negotiation patterns. Understanding these interactions is necessary to determine where an attack occurs: in the protocol itself, in the host or client, in the server, in a tool's implementation, or in the configuration that connects these components.

The specification explains protocol behaviour; security guidance explains how implementations should handle trust, authentication, authorisation, input validation, tool execution, and other security-sensitive operations. A protocol can define a communication mechanism without automatically guaranteeing that every connected server is trustworthy or that every tool call is safe.

### Security significance

The main lesson is to avoid treating MCP as a complete security boundary. A correctly formatted MCP message does not necessarily represent a safe request. The security of an MCP-based system depends on the behaviour of the host, client, server, model, tool, and surrounding environment.

For example, a tool can be described correctly at the protocol level but still perform an unsafe operation if its implementation fails to validate arguments or enforce authorisation. Similarly, a model may receive malicious instructions in a tool description or resource and then make an unsafe tool call, even if the underlying messages are protocol-compliant.

---

## 2. [“Breaking the Protocol: Security Analysis of the Model Context Protocol Specification and Prompt Injection Vulnerabilities in Tool-Integrated LLM Agents”](https://arxiv.org/abs/2601.17549) 

### Summary

This paper examines MCP security from an architectural and protocol-design perspective, with particular attention to prompt injection in systems where language models can call external tools. Its central argument is that some risks may arise not only from individual insecure server implementations, but also from the way trust and authority are represented and propagated across MCP interactions.

The paper identifies three main issues:

1. **Lack of capability attestation.** A server may claim to provide particular capabilities or permissions without a strong mechanism for independently verifying that claim. If a host or model trusts tool descriptions or capability declarations too readily, it may grant the server more influence than is appropriate.
2. **Sampling and origin authentication.** MCP sampling allows a server to send requests to the LLM through the client. The authors argue that insufficiently authenticated or clearly separated origins for content can allow server-supplied instructions to influence the model as though they were trusted instructions.
3. **Implicit trust propagation across multiple servers.** When an agent interacts with several servers, information or instructions originating from one component may influence actions involving another. This can create a chain of trust in which content from a less-trusted source affects access to a more-sensitive capability.

The paper introduces **MCPBench**, a framework for evaluating attacks in MCP-compatible settings, and reports controlled experiments across multiple server implementations. It also proposes **MCPSec**, a protocol extension intended to add stronger capability attestation and message authentication. The paper reports that these changes reduced attack success in its evaluated scenarios, with some additional message latency.

These findings are the authors' experimental results and proposals. They should be examined in the context of the specific benchmark, implementations, versions, and assumptions used in the paper.

### Security significance

This work is especially useful for thinking about the difference between **protocol-level weaknesses** and **implementation-level weaknesses**.

A server may be malicious or compromised, but a system's architecture can determine how much influence that server can exert. If the host cannot reliably establish the origin of instructions, distinguish trusted policy from untrusted content, or constrain a server's capabilities, then prompt injection can become a route to unauthorised actions.

The sampling discussion is particularly relevant because sampling is a server-to-client request that can lead to model generation. More importance should be placed on what context the client sends to the model, how the request is presented, and whether the server can cause the model to act on instructions that conflict with the user's intent or host policy.

---

## 3. [“Model Context Protocol (MCP): Security Design Considerations for AI-Driven Automation”](https://www.nsa.gov/Portals/75/documents/Cybersecurity/CSI_MCP_SECURITY.pdf)  


### Summary

This cybersecurity information sheet discusses security risks associated with using MCP to connect AI systems to tools, data, and automated workflows. It emphasises that MCP adoption has moved quickly and that the security model, implementation practices, and operational controls must keep pace.

A key theme is that MCP-related risk cannot be understood by examining only one endpoint or one message. An agentic workflow connects several components, and trust decisions made at one point can affect later actions. A weakness in a server, client, model-facing context, permission configuration, or deployment environment may combine with other weaknesses to produce a larger failure.

The report draws attention to risks associated with the dynamic invocation of tools, implicit trust relationships, context sharing, and the execution of actions by AI-driven systems. Traditional controls such as authentication, authorisation, and input validation remain necessary, but they may not be sufficient on their own when a model interprets untrusted content and decides which tools to call.

The guidance also highlights the need to consider the wider system lifecycle: which tools are available, how they are configured, what information is passed between components, what actions the agent can take, and how those actions are monitored. Security should therefore be addressed through layered controls rather than relying on the model to recognise malicious instructions.

### Security significance

The report is useful because it frames MCP security as a combination of protocol design, implementation, and operational governance. For example, a system might implement authentication correctly yet still expose sensitive actions through overly broad permissions. Alternatively, a tool might be technically legitimate but have a description or output that manipulates the model into using it in an unintended way.

The report also provides a practical security perspective that complements academic attack taxonomies. It can help translate a demonstrated attack into a discussion of realistic deployment conditions, organisational controls, monitoring, and remediation.

---

## 4. [“MCPTox: A Benchmark for Tool Poisoning Attack on Real-World MCP Servers”](https://arxiv.org/abs/2508.14925)

### Summary

This paper investigates **tool poisoning attacks**, in which malicious instructions are embedded in a tool's metadata, such as its description, rather than relying only on malicious code executing inside the tool. When an MCP client or host discovers tools, it may pass their descriptions to the language model. A poisoned description can therefore attempt to influence the model's decisions about which tools to call, what arguments to supply, or what actions to take.

The paper introduces **MCPTox**, a benchmark designed to evaluate how well LLM agents resist tool poisoning in more realistic MCP settings. The benchmark uses tools from real MCP servers and evaluates multiple agent/model configurations against generated malicious test cases. It examines multiple attack patterns and risk categories rather than relying on a single illustrative demonstration.

The authors report substantial vulnerability across the evaluated systems. The published abstract reports an attack success rate of 72.8% for o1-mini and refusal rates below 3% even for the model with the highest refusal rate in the evaluation. The paper argues that more capable models can sometimes be more susceptible because their instruction-following abilities may make them more likely to follow malicious instructions embedded in tool metadata.

The result is important because the poisoned tool does not necessarily need to execute malicious code. The attack targets the model's interpretation of the tool description and its subsequent use of an otherwise legitimate tool. A conventional approval step may not fully address this if the user sees the requested action but not the untrusted instructions that influenced the model to request it.

### Security significance

MCPTox provides empirical evidence that tool metadata should not automatically be treated as trustworthy instructions. Tool descriptions are often needed to help a model understand how to use a capability, but they can also carry instructions that are irrelevant, misleading, or malicious.

The study also illustrates why model safety alignment alone may not be a reliable defence. If a poisoned description persuades the model to perform an apparently ordinary action through a legitimate tool, a model's general refusal behaviour may not recognise the action as unsafe. Stronger controls may need to exist outside the model, including trusted tool registries, provenance checks, least-privilege permissions, policy enforcement, and validation of sensitive actions.

---

## 5. [“Systematic Analysis of MCP Security”](https://arxiv.org/abs/2508.12538)

### Summary

This paper aims to provide a broader and more systematic view of MCP security than studies focused on a single vulnerability. It introduces **MCPLib**, an MCP attack library and taxonomy containing 31 attack methods grouped into four broad categories:

1. **Direct tool injection attacks**
2. **Indirect tool injection attacks**
3. **Malicious user attacks**
4. **LLM-inherent attacks**

The categories distinguish attacks according to how malicious influence enters the system and which part of the agent/tool interaction is targeted. For example, direct tool injection can involve malicious content in tool descriptions or attributes. Indirect attacks can exploit external data, files, or connected services that later influence the agent. Malicious-user attacks begin with an adversarial user request, while LLM-inherent attacks exploit weaknesses in the model's reasoning or instruction handling.

The authors use the taxonomy and attack library to evaluate different attack methods. Their reported observations include agents relying too heavily on tool descriptions, susceptibility to file-based attacks, chain attacks that exploit shared context, and difficulty distinguishing external data from instructions or executable commands.

The main contribution is both conceptual and practical: a structured classification of attack methods, a common framework for implementing or examining them, and experimental analysis of their effectiveness. This helps researchers move from isolated examples to a more consistent approach for describing and comparing attack surfaces.

### Security significance

A taxonomy helps reveal that MCP security is not one problem. Attacks can originate from different actors, enter through different components, and exploit different trust assumptions. A defence that addresses malicious tool descriptions may not prevent a malicious user request or an indirect prompt injection in a resource. Similarly, an attack may require several components to interact before it produces a security impact.

The taxonomy can also help identify overlap between attack names. Two attacks may share the same underlying mechanism but differ in the entry point, attacker capability, or impact. 

---

## 6. [“Securing the Model Context Protocol (MCP): Risks, Controls, and Governance”](https://arxiv.org/abs/2511.20920)  

### Summary

This paper considers the risks that emerge when MCP replaces static, developer-controlled integrations with more dynamic agent systems that can discover and use tools. It focuses not only on individual technical vulnerabilities, but also on the controls and governance needed to operate MCP-based systems responsibly.

The paper discusses three broad adversarial situations:

1. **Content-injection attackers**, who embed malicious instructions in otherwise legitimate data or content that an agent processes.
2. **Supply-chain attackers**, who distribute compromised or untrustworthy MCP servers or tools.
3. **Agents acting beyond their intended role**, where the agent's tool use or decisions exceed the user's intent or the permissions that should apply.

The authors discuss risks such as data exfiltration, tool poisoning, and cross-system privilege escalation. They propose controls including per-user authentication and scoped authorisation, provenance tracking across agent workflows, sandboxing, input/output checks, inline policy enforcement, data-loss prevention (DLP), anomaly detection, and centralised governance through private registries or gateway layers.

The central idea is that securing an MCP deployment requires more than trusting the model or securing the network connection. Organisations need to control which tools are available, who can use them, what data can flow between them, what actions are permitted, and how those actions are audited.

### Security significance

This paper connects technical attack mechanisms with operational controls. For example, a poisoned tool description is a content-injection problem, but its impact may depend on whether the tool can access sensitive data, whether actions are restricted by per-user permissions, whether outputs are monitored, and whether the organisation can identify which tool version was used.

Likewise, a compromised tool is a supply-chain problem, but risk can be reduced through trusted distribution, version management, isolation, restricted privileges, and auditing. These controls may not eliminate every attack, but they can reduce the probability or impact of compromise.

The governance perspective is useful because some controls are organisational rather than protocol-level. A private registry or approval process may be appropriate for an enterprise deployment even if it is not part of the MCP specification itself.

---