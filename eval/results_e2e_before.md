# End-to-end evaluation results

Questions: 19 (13 answerable, 6 out-of-scope). LLM: `openai/gpt-oss-120b`.

| Metric | Result |
|---|---:|
| Answerable questions answered (not refused) | 77% |
| Source-file Hit@5 (questions with expected file: 8) | 75% |
| Source-file MRR | 0.51 |
| Refusal accuracy on out-of-scope | 100% |
| Numbers in answers found in cited passages (automatic) | 93% |
| Mean end-to-end latency | 4.4s |

Answer correctness is NOT auto-scored: fill the `Correct?` column by reading each answer against the PDF page.

| ID | Question | Answered | Gate refused | Conf | Rank | Cited sources (file p.page) | Numbers ok | Correct? |
|---|---|---|---|---:|---:|---|---|---|
| pk1 | How much assistance does PM-KISAN provide? | False | False | 0.65 | - | - | - | |
| pk2 | Who can receive PM-KISAN benefits? | True | False | 0.67 | 1 | RevisedPM-KISANOperationalGuidelines(English).pdf p.3; RevisedPM-KISANOperationalGuidelines(English).pdf p.4; RevisedPM-KISANOperationalGuidelines(English).pdf p.5 | 3/3 | |
| jay1 | What health cover does PM-JAY provide? | True | False | 0.54 | 1 | ayush.pdf p.2 | - | |
| jay2 | What are the eligibility rules for PM-JAY? | False | False | 0.46 | - | - | - | |
| sc1 | Who is eligible for the SC post-matric scholarship? | True | False | 0.80 | 4 | Guidelines-to-post-matric-scholaships-to-the-students-belonging-to-scheduled-castes-for-students-in-India-2020-2021-to-2025-26_0001.pdf p.7; gr6_dscw_sje_02092022.pdf p.3; gr6_dscw_sje_02092022.pdf p.6; gr6_dscw_sje_02092022.pdf p.8 | 4/4 | |
| sc2 | What expenses does the post-matric scholarship cover? | True | False | 0.70 | 1 | Guidelines-to-post-matric-scholaships-to-the-students-belonging-to-scheduled-castes-for-students-in-India-2020-2021-to-2025-26_0001.pdf p.6; gr6_dscw_sje_02092022.pdf p.7 | - | |
| pk1r | Tell me the yearly PM Kisan support amount. | True | False | 0.62 | 2 | RevisedPM-KISANOperationalGuidelines(English).pdf p.2 | 1/1 | |
| sc1r | Which students qualify for the SC post-matric award? | True | False | 0.65 | 3 | Guidelines-to-post-matric-scholaships-to-the-students-belonging-to-scheduled-castes-for-students-in-India-2020-2021-to-2025-26_0001.pdf p.2; Guidelines-to-post-matric-scholaships-to-the-students-belonging-to-scheduled-castes-for-students-in-India-2020-2021-to-2025-26_0001.pdf p.7; gr6_dscw_sje_02092022.pdf p.3; gr6_dscw_sje_02092022.pdf p.6 | 4/4 | |
| oos1 | What is the PM-KISAN amount in Bangladesh? | False | False | 0.54 | - | - | - | |
| oos2 | How do I apply for PM Awas Yojana? | False | False | 0.49 | - | - | - | |
| oos3 | Who won the 2023 cricket world cup? | False | False | 0.22 | - | - | - | |
| pk3 | Is Aadhaar compulsory to receive PM-KISAN benefits? | True | False | 0.62 | - | RevisedPM-KISANOperationalGuidelines(English).pdf p.6 | - | |
| pk4 | How is a family defined under PM-KISAN? | True | False | 0.62 | - | RevisedPM-KISANOperationalGuidelines(English).pdf p.2 | - | |
| jay3 | What is the health cover per family per year under PM-JAY? | True | False | 0.58 | - | 2022051036.pdf p.1; AMH.pdf p.1; ayush.pdf p.2 | - | |
| sc3 | What is the annual parental income limit for the SC post-matric scholarship? | True | False | 0.77 | - | gr6_dscw_sje_02092022.pdf p.6 | 1/2 | |
| sc4 | Are students doing correspondence or online courses eligible for the SC post-matric scholarship? | False | False | 0.76 | - | - | - | |
| oos4 | What is the PM-JAY health cover in the USA? | False | False | 0.53 | - | - | - | |
| oos5 | Who is the current Agriculture Minister of India? | False | False | 0.53 | - | - | - | |
| oos6 | What will the PM-KISAN installment amount be in 2030? | False | False | 0.56 | - | - | - | |

## Answers

**pk1** How much assistance does PM-KISAN provide?

I don't know based on the provided documents.

**pk2** Who can receive PM-KISAN benefits?

PM‑KISAN benefits are paid to the people whose names are uploaded on the PM‑Kisan portal for a given trimester.  According to the operational guidelines, the eligible groups include  

* **Land‑holding farmer families** whose cultivable‑land records are uploaded (beneficiaries continue to receive installments for the whole financial year) [1].  
* **Employees of local bodies** (but not Multi‑Tasking Staff, Class IV or Group D employees) [2].  
* **Superannuated/retired pensioners** whose monthly pension is ₹10,000 or more (excluding the same staff categories) [2].  
* **Persons who paid income tax** in the last assessment year [2].  
* **Registered professionals** – doctors, engineers, lawyers, chartered accountants and architects who are practising members of their professional bodies [2].  

People who acquire cultivable land by transfer (other than inheritance) are **not** entitled to benefits, and land‑holding farmer families who are NRIs are also excluded [2].  If land ownership changes by inheritance, eligibility is reassessed; if the new family remains eligible, they continue to receive benefits [3].

**Summary:** PM‑Kisan benefits go to uploaded land‑holding farmer families and, per the guidelines, also to local‑body employees, pensioners with ≥₹10 000 pension, recent income‑tax payers, and practising registered professionals, while transferees (non‑inheritance) and NRIs are excluded.

**jay1** What health cover does PM-JAY provide?

PM‑JAY provides secondary and tertiary health coverage of up to ₹5 lakh per family[3].  
**Summary:** The scheme covers inpatient (secondary/tertiary) care for each family up to ₹5 lakh.

**jay2** What are the eligibility rules for PM-JAY?

I don't know based on the provided documents.

**sc1** Who is eligible for the SC post-matric scholarship?

The SC post‑matric scholarship is for Indian nationals who:

* Belong to the Scheduled Castes recognized by the State/UT in which they are domiciled [3]  
* Have passed the Matriculation, Higher Secondary or any higher examination of a recognized board/university [3]  
* Have a family annual income of up to Rs 2.50 lakh [4][5]  
* Are studying in India, with the awardee selected by the State/UT to which they belong [2]  

In addition, the scheme gives special priority to the poorest households, namely:

* SC households with three or more deprivations as per SECC‑2011 [4][5]  
* SC households where one or both parents are illiterate [4][5]  
* Students who passed 10th standard from a State Government/ Municipality/Local Body school [4][5]  

**Summary:** Indian SC students with ≤ Rs 2.5 lakh family income, who have passed matric or higher, and meet any of the listed deprivation criteria are eligible.

**sc2** What expenses does the post-matric scholarship cover?

The post‑matric scholarship for Scheduled Castes can be used for books, equipment, and board‑and‑lodging expenses in addition to the cash allowance [1][2].

**Summary:** It covers books, equipment and living (board‑and‑lodging) costs.

**pk1r** Tell me the yearly PM Kisan support amount.

The PM‑Kisan scheme provides **Rs 6,000 per year** to each eligible farmer family[1].  
**Summary:** Yearly support under PM‑Kisan is Rs 6,000.

**sc1r** Which students qualify for the SC post-matric award?

Students who meet **all** of the following conditions qualify for the SC post‑matric scholarship:

* Indian nationals [4]  
* Belong to a Scheduled Caste as defined by the State/UT of permanent domicile [4]  
* Have passed Matriculation, Higher Secondary or any higher examination of a recognized board or university [4]  
* Have a family annual income of up to **Rs 2.50 lakh** [5]  
* Are studying in India and are selected by the State/UT to which they belong [2][3]  

The scheme gives special priority to the poorest households, i.e., SC students who (i) have three or more deprivations under SECC‑2011, (ii) have one or both parents illiterate, or (iii) passed 10th standard from a government/municipal school [5].

**Summary:** SC students who are Indian, domiciled in a State/UT, have passed Matric/Higher Secondary, earn ≤ Rs 2.5 lakh annually, and study in India (with extra focus on the poorest households) qualify.

**oos1** What is the PM-KISAN amount in Bangladesh?

I don't know based on the provided documents.

**oos2** How do I apply for PM Awas Yojana?

I don't know based on the provided documents.

**oos3** Who won the 2023 cricket world cup?

I don't know based on the provided documents.

**pk3** Is Aadhaar compulsory to receive PM-KISAN benefits?

The PM‑KISAN guidelines do not state that Aadhaar is mandatory to receive the benefit. They require beneficiaries to give consent for their Aadhaar number to be used for eligibility verification, but they do not make Aadhaar compulsory for receiving the payment[5].  

**Summary:** Aadhaar is not compulsory for PM‑KISAN; it is optional and used only with the beneficiary’s consent.

**pk4** How is a family defined under PM-KISAN?

A “farmer’s family” under PM‑KISAN is defined as **a family consisting of the husband, wife and minor children who own cultivable land according to the land records of the relevant State/UT**[2].  

**Summary:** The scheme’s family unit is the husband, wife and minor children who hold cultivable land in official records.

**jay3** What is the health cover per family per year under PM-JAY?

The health‑cover under PM‑JAY is **₹5 lakh per family per year** on a family‑floater basis[1][2][3].  

**Summary:** PM‑JAY provides a ₹5 lakh annual health cover for each beneficiary family.

**sc3** What is the annual parental income limit for the SC post-matric scholarship?

The annual parental/guardian income limit for the SC post‑matric scholarship is **Rs 2,50,000** per year[2].  
**Summary:** Eligible SC students must have parents’/guardians’ income ≤ Rs 2.5 lakh.

**sc4** Are students doing correspondence or online courses eligible for the SC post-matric scholarship?

I don't know based on the provided documents.

**oos4** What is the PM-JAY health cover in the USA?

I don't know based on the provided documents.

**oos5** Who is the current Agriculture Minister of India?

I don't know based on the provided documents.

**oos6** What will the PM-KISAN installment amount be in 2030?

I don't know based on the provided documents.

## Auto-flagged failure candidates (review these, then write the root cause)

- `pk1`: answerable but the system said 'I don't know'
- `pk1`: expected file `PMKisanSamanNidhi.pdf` not in top-5
- `jay2`: answerable but the system said 'I don't know'
- `jay2`: expected file `AMH.pdf` not in top-5
- `sc3`: numbers not found in cited passages: ['2.5']
- `sc4`: answerable but the system said 'I don't know'

Known finding: the similarity gate does not separate in-scope from out-of-scope queries (MiniLM scores unrelated questions high), so refusal depends on the LLM prompt.
