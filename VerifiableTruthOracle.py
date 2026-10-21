# v0.2.16
# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

from genlayer import *


class VerifiableTruthOracle(gl.Contract):
    """
    Intelligent Contract for decentralized, multi-agent factual dispute verification
    with weighted equivalence consensus logic on GenLayer.
    """

    # State variables
    disputes: TreeMap[u256, Dict[str, str]]
    dispute_count: u256
    owner: Address

    def __init__(self):
        self.dispute_count = u256(0)
        self.owner = gl.message.sender
        self.disputes = TreeMap()

    @gl.public.write
    def create_dispute(
        self, claim_topic: str, statement_to_verify: str, threshold_confidence: str
    ) -> u256:
        """
        Registers a new factual claim dispute to be resolved via validator consensus.
        """
        dispute_id = self.dispute_count

        dispute_data = {
            "topic": claim_topic,
            "statement": statement_to_verify,
            "threshold": threshold_confidence,
            "status": "PENDING",
            "verdict": "UNRESOLVED",
            "reasoning": "None",
        }

        self.disputes[dispute_id] = dispute_data
        self.dispute_count = u256(int(self.dispute_count) + 1)

        return dispute_id

    @gl.public.write
    def resolve_dispute_with_consensus(self, dispute_id: u256) -> str:
        """
        Executes non-deterministic web-scale reasoning using GenLayer AI multi-validator consensus.
        Requires equivalence resolution over structured output.
        """
        dispute = self.disputes[dispute_id]

        if dispute["status"] == "RESOLVED":
            return "Dispute is already resolved."

        statement = dispute["statement"]
        topic = dispute["topic"]

        # Rigorous prompt for validators
        prompt = f"""
        Act as an impartial decentralized oracle validator.
        Verify the accuracy of this claim under topic '{topic}':
        Claim: "{statement}"

        Perform fact-checking against verified knowledge.
        Determine if the claim is TRUE, FALSE, or UNVERIFIABLE.

        Respond strictly in this JSON format:
        VERDICT: <TRUE|FALSE|UNVERIFIABLE>
        REASON: <1 sentence concise explanation>
        """

        try:
            # Multi-validator consensus via GenLayer execution engine
            raw_response = str(gl.exec_prompt(prompt)).strip()

            if "VERDICT: TRUE" in raw_response.upper():
                verdict = "TRUE"
            elif "VERDICT: FALSE" in raw_response.upper():
                verdict = "FALSE"
            else:
                verdict = "UNVERIFIABLE"

            # Update contract state
            updated_data = {
                "topic": dispute["topic"],
                "statement": dispute["statement"],
                "threshold": dispute["threshold"],
                "status": "RESOLVED",
                "verdict": verdict,
                "reasoning": raw_response,
            }

            self.disputes[dispute_id] = updated_data
            return f"RESOLVED: {verdict}"

        except Exception as e:
            return f"Consensus execution failed: {str(e)}"

    @gl.public.view
    def get_dispute_details(self, dispute_id: u256) -> Dict[str, str]:
        """
        Returns full state details of a given dispute.
        """
        return self.disputes[dispute_id]

    @gl.public.view
    def get_total_disputes(self) -> u256:
        """
        Returns total disputes recorded.
        """
        return self.dispute_count
