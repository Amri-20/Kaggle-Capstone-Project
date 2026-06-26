import unittest
from backend.utils.reports import generate_markdown_report

class TestReports(unittest.TestCase):
    def test_markdown_generation(self):
        data = {
            "title": "Carbon Tracking App",
            "executive_summary": "An executive summary test.",
            "swot": {
                "strengths": ["Scalable"],
                "weaknesses": ["Cost"],
                "opportunities": ["Green growth"],
                "threats": ["Rules"]
            },
            "risks": [
                {"description": "GDPR leak", "severity": "High", "likelihood": "Low", "mitigation": "Encryption"}
            ],
            "financials": {
                "budget": "$100,000",
                "roi_3yr": "120%"
            },
            "tech_review": {
                "feasibility": "High",
                "tech_stack": "FastAPI, SQLite"
            },
            "decision_score": 90,
            "recommendation": "Highly Recommended",
            "action_plan": [
                {"phase": "Phase 1: Setup", "details": "Launch the repository"}
            ]
        }
        
        report = generate_markdown_report(data)
        self.assertIsNotNone(report)
        self.assertIn("Carbon Tracking App", report)
        self.assertIn("SWOT Analysis", report)
        self.assertIn("Decision Score: 90", report)
        self.assertIn("GDPR leak", report)

if __name__ == "__main__":
    unittest.main()
