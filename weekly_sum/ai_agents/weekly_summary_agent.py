#uvicorn app.api:app --reload
#127.0.0.1:8000/docs
# {
#  "completed": [
#    "Login API finished",
#    "CI/CD pipeline setup"
#  ],
#  "delayed": [
#    "Analytics module due to missing data"
#  ],
#  "notes": "Customer emphasized analytics importance during weekly meeting."
#}

import os
import json
from ai.google_ai import GoogleAIClient


def extract_json(response_raw: str) -> dict:

    if not response_raw or response_raw.strip() == "":
        raise ValueError("AI returned an empty response — cannot parse JSON.")

    # 1) Backtick temizle
    cleaned = response_raw.replace("```json", "").replace("```", "").strip()

    # 2) JSON’un ilk '{' noktasını bul
    start = cleaned.find("{")
    end = cleaned.rfind("}")

    if start == -1 or end == -1:
        print("RAW RESPONSE BY AI (for debugging):\n", response_raw)
        raise ValueError("No JSON object found in AI response.")

    json_str = cleaned[start:end + 1]

    # 3) JSON parse etmeyi dene
    try:
        return json.loads(json_str)
    except Exception as e:
        print("❌ JSON parsing failed!")
        print("Extracted JSON string:\n", json_str)
        print("Raw response:\n", response_raw)
        raise e


class WeeklySummaryAgent:
    def __init__(self):
        self.model = GoogleAIClient()

    def generate_summary(self, data: dict, save_to_file: bool = True) -> dict:

        prompt = f"""
        You are an AI project management assistant.
        Create a clean WEEKLY SUMMARY using the data below.
        Return ONLY JSON. Do NOT add any explanations.

        DATA:
        {data}

        JSON fields must be:
        - summary
        - accomplishments
        - risks
        - next_week_plan
        - suggestions
        """

        # 1) Raw AI yanıtını al
        response_raw = self.model.send_message(prompt)

        # 2) JSON'u güvenli şekilde çıkar
        summary_json = extract_json(response_raw)

        # 3) Output'a kaydet
        if save_to_file:
            self.save_summary(summary_json)

        return summary_json

    def save_summary(self, summary_json: dict):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        output_path = os.path.join(base_dir, "..", "outputs", "weekly_summary.json")
        output_path = os.path.abspath(output_path)

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, "w") as f:
            json.dump(summary_json, f, indent=4)

        print(f"📄 Saved weekly summary to: {output_path}")
