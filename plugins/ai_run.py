import os
import json
from typing import Optional, List

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field


load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# -----------------------------
# JSON SCHEMA
# -----------------------------

class PersonalDetails(BaseModel):
    admission_no: Optional[str] = None
    roll_no: Optional[str] = None
    name: Optional[str] = None
    course: Optional[str] = None
    branch: Optional[str] = None
    semester: Optional[str] = None
    gender: Optional[str] = None
    dob: Optional[str] = None
    nationality: Optional[str] = None
    religion: Optional[str] = None
    entrance_type: Optional[str] = None
    rank: Optional[str] = None
    seat_type: Optional[str] = None
    category_caste: Optional[str] = None
    last_studied: Optional[str] = None
    joining_date: Optional[str] = None
    phone_no: Optional[str] = None
    mobile_no: Optional[str] = None
    email: Optional[str] = None
    bank_account_no: Optional[str] = None
    aadhar_no: Optional[str] = None
    ration_card_no: Optional[str] = None
    scholarship: Optional[str] = None


class Education(BaseModel):
    qualification: Optional[str] = None
    board: Optional[str] = None
    hall_ticket_no: Optional[str] = None
    year_of_pass: Optional[str] = None
    institute: Optional[str] = None
    max_marks: Optional[str] = None
    obtained_marks: Optional[str] = None
    grade: Optional[str] = None
    grade_points: Optional[str] = None


class ParentDetails(BaseModel):
    father_name: Optional[str] = None
    father_occupation: Optional[str] = None
    mother_name: Optional[str] = None
    mother_occupation: Optional[str] = None
    phone_no: Optional[str] = None
    father_mobile_no: Optional[str] = None
    mother_mobile_no: Optional[str] = None
    annual_income: Optional[str] = None
    father_email: Optional[str] = None
    mother_email: Optional[str] = None
    correspondence_address: Optional[str] = None
    permanent_address: Optional[str] = None


class GuardianDetails(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    mobile: Optional[str] = None


class AttendanceRecord(BaseModel):
    serial_no: Optional[int] = None
    subject: Optional[str] = None
    held: Optional[int] = None
    attended: Optional[int] = None
    percentage: Optional[float] = None


class Attendance(BaseModel):
    subjects: List[AttendanceRecord] = Field(default_factory=list)
    total_held: Optional[int] = None
    total_attended: Optional[int] = None
    total_percentage: Optional[float] = None


class FeeRecord(BaseModel):
    year: Optional[str] = None
    fee_type: Optional[str] = None
    fee_amount: Optional[str] = None
    concession: Optional[str] = None
    payable: Optional[str] = None
    paid: Optional[str] = None
    receipt_numbers: List[str] = Field(default_factory=list)
    receipt_dates: List[str] = Field(default_factory=list)
    due: Optional[str] = None
    excess_paid: Optional[str] = None
    refund: Optional[str] = None


class Fees(BaseModel):
    records: List[FeeRecord] = Field(default_factory=list)
    grand_total_fee: Optional[str] = None
    grand_total_payable: Optional[str] = None
    grand_total_paid: Optional[str] = None
    balance: Optional[str] = None


class StudentData(BaseModel):
    personal_details: PersonalDetails
    education: List[Education] = Field(default_factory=list)
    parent_details: ParentDetails
    guardian_details: GuardianDetails
    attendance: Attendance
    fees: Fees
    achievements: List[str] = Field(default_factory=list)
    paper_presentations: List[str] = Field(default_factory=list)


# -----------------------------
# AI EXTRACTION
# -----------------------------

def extract_student_data(scraped_data: dict):

    prompt = f"""
You are a highly accurate document-data extraction system.

Extract information from the scraped student record and return it
STRICTLY according to the provided schema.

IMPORTANT RULES:

1. Extract ONLY information actually present in the input.
2. NEVER invent, guess, or modify values.
3. If a field is empty, return null.
4. Preserve names, numbers, dates and IDs exactly as they appear.
5. Do NOT move a value from one field to another.
6. A label belongs only to the value immediately associated with that label.
7. Pay special attention to:
   - Name
   - Phone.No
   - Mobile.No
   - Father Mobile.No
   - Mother Mobile.No
   - Rank
   - Seat Type
   - Addresses
8. "Rank" and "Seat Type" are separate fields.
9. "Name" must contain the value after "Name :" and nothing else.
10. Do NOT interpret another field's label as a value.
11. Parse attendance rows individually.
12. Parse fee rows individually.
13. Keep receipt numbers and receipt dates associated with the correct fee.
14. Preserve leading zeros if any.
15. Do not calculate missing values.
16. Do not correct values using outside knowledge.
17. If information is ambiguous, return null instead of guessing.

The input contains several sections:
- Personal Details
- Education Details
- Parent's Details
- Guardian Details
- Attendance
- Fees
- Achievements
- Paper Presentations

SCRAPED DATA:

{json.dumps(scraped_data, ensure_ascii=False, indent=2)}
"""

    response = client.chat.completions.parse(
        model="gpt-5.6-luna",
        messages=[
            {
                "role": "system",
                "content": "You extract structured data from scraped student records. Accuracy is more important than completeness."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        response_format=StudentData
    )

    parsed = response.choices[0].message.parsed

    if parsed is None:
        raise ValueError("AI failed to parse the student data")

    return parsed.model_dump()
