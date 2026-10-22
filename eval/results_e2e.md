# End-to-end evaluation results

Questions: 19 (13 answerable, 6 out-of-scope). LLM: `openai/gpt-oss-120b`.

| Metric | Result |
|---|---:|
| Answerable questions answered (not refused) | 92% |
| Source-file Hit@5 (questions with expected file: 8) | 75% |
| Source-file MRR | 0.69 |
| Refusal accuracy on out-of-scope | 100% |
| Numbers in answers found in cited passages (automatic) | 93% |
| Mean end-to-end latency | 4.6s |

Answer correctness is NOT auto-scored: fill the `Correct?` column by reading each answer against the PDF page.

| ID | Question | Answered | Gate refused | Conf | Rank | Cited sources (file p.page) | Numbers ok | Correct? |
|---|---|---|---|---:|---:|---|---|---|
| pk1 | How much assistance does PM-KISAN provide? | False | False | 0.65 | - | - | - | |
| pk2 | Who can receive PM-KISAN benefits? | True | False | 0.67 | 1 | RevisedPM-KISANOperationalGuidelines(English).pdf p.3; RevisedPM-KISANOperationalGuidelines(English).pdf p.5 | 1/1 | |
| jay1 | What health cover does PM-JAY provide? | True | False | 0.54 | 1 | ayush.pdf p.2; ayush.pdf p.9 | - | |
| jay2 | What are the eligibility rules for PM-JAY? | True | False | 0.46 | - | 2022050996.pdf p.22; 2022051036.pdf p.8 | - | |
| sc1 | Who is eligible for the SC post-matric scholarship? | True | False | 0.80 | 1 | gr6_dscw_sje_02092022.pdf p.3; gr6_dscw_sje_02092022.pdf p.6; gr6_dscw_sje_02092022.pdf p.8 | - | |
| sc2 | What expenses does the post-matric scholarship cover? | True | False | 0.70 | 1 | gr6_dscw_sje_02092022.pdf p.7 | - | |
| pk1r | Tell me the yearly PM Kisan support amount. | True | False | 0.62 | 2 | RevisedPM-KISANOperationalGuidelines(English).pdf p.2 | 1/1 | |
| sc1r | Which students qualify for the SC post-matric award? | True | False | 0.65 | 1 | gr6_dscw_sje_02092022.pdf p.6; gr6_dscw_sje_02092022.pdf p.8 | 6/6 | |
| oos1 | What is the PM-KISAN amount in Bangladesh? | False | False | 0.54 | - | - | - | |
| oos2 | How do I apply for PM Awas Yojana? | False | False | 0.49 | - | - | - | |
| oos3 | Who won the 2023 cricket world cup? | False | False | 0.22 | - | - | - | |
| pk3 | Is Aadhaar compulsory to receive PM-KISAN benefits? | True | False | 0.62 | - | PMKisanSamanNidhi.pdf p.2; RevisedPM-KISANOperationalGuidelines(English).pdf p.8; RevisedPM-KISANOperationalGuidelines(English).pdf p.10 | 4/4 | |
| pk4 | How is a family defined under PM-KISAN? | True | False | 0.62 | - | RevisedPM-KISANOperationalGuidelines(English).pdf p.2 | - | |
| jay3 | What is the health cover per family per year under PM-JAY? | True | False | 0.58 | - | AMH.pdf p.1; ayush.pdf p.2 | - | |
| sc3 | What is the annual parental income limit for the SC post-matric scholarship? | True | False | 0.77 | - | gr6_dscw_sje_02092022.pdf p.6 | 1/2 | |
| sc4 | Are students doing correspondence or online courses eligible for the SC post-matric scholarship? | True | False | 0.76 | - | gr6_dscw_sje_02092022.pdf p.6 | - | |
| oos4 | What is the PM-JAY health cover in the USA? | False | False | 0.53 | - | - | - | |
| oos5 | Who is the current Agriculture Minister of India? | False | False | 0.53 | - | - | - | |
| oos6 | What will the PM-KISAN installment amount be in 2030? | False | False | 0.56 | - | - | - | |

## Answers

**pk1** How much assistance does PM-KISAN provide?

I don't know based on the provided documents.

**pk2** Who can receive PM-KISAN benefits?

PM‑KISAN benefits are paid to :

* Farmers’ families who own cultivable land (their names are uploaded on the PM‑Kisan portal) [1]  
* Employees of local bodies, except multitasking staff/Class IV/Group D employees [2]  
* Superannuated/retired pensioners whose monthly pension is ₹10,000 or more (excluding multitasking staff/Class IV/Group D) [2]  
* Anyone who paid income‑tax in the last assessment year [2]  
* Professionals such as doctors, engineers, lawyers, chartered accountants and architects who are registered with their professional bodies and practice [2]  

NRIs (non‑resident Indians) who are land‑holding farmers are excluded [2].

**Summary:** PM‑Kisan benefits go to cultivable‑land‑owning farmer families and certain eligible workers, pensioners, taxpayers and registered professionals, but not to NRIs.

**jay1** What health cover does PM-JAY provide?

PM‑JAY (Ayushman Bharat) offers secondary and tertiary health coverage of **₹5 lakh per family**. The scheme’s “Golden card” does **not cover OPD (out‑patient) treatment**, so any OPD costs must be paid by the patient[3][4].  

*PM‑JAY provides up to ₹5 lakh of secondary/tertiary coverage, but no OPD benefits.*

**jay2** What are the eligibility rules for PM-JAY?

PM‑JAY eligibility is defined at two levels in the documents:

* **Beneficiary eligibility** – A family must be listed among the “eligible families” in the state‑specific scheme.  Beneficiaries must present an Aadhaar number, or if they do not have Aadhaar, any other valid government ID (e.g., Ration Card or a state‑issued family ID) when they seek care[5].  

* **Provider eligibility** – Hospitals and clinics can be empanelled only if they have the required staff and infrastructure.  A qualified doctor must be an MBBS‑qualified practitioner as per the Clinical Establishment Act or state rules, and a qualified nurse must also be available.  The facility must have the specified emergency equipment and other resources[1].  

**Summary:** Families listed in the state‑approved eligible‑family list can use PM‑JAY if they show Aadhaar or another government ID, and only providers meeting the prescribed staff‑qualification and equipment standards may deliver services.

**sc1** Who is eligible for the SC post-matric scholarship?

Eligible candidates are:

* Indian nationals only [3]  
* Belong to the Scheduled Castes as defined for the State/UT in which they are domiciled [3]  
* Have passed the Matriculation, Higher‑Secondary or any higher examination of a recognized university/board [3]  
* Have a family annual income not exceeding the prescribed ceiling for SC students [1]  
* Intend to pursue studies in India and are selected by the State/UT to which they belong [2]  

**Summary:** SC post‑matric scholarships are for Indian SC students from the applicant’s domicile state, with qualifying exam results, low family income, and study plans within India.

**sc2** What expenses does the post-matric scholarship cover?

The post‑matric scholarship can be used for books, equipment and board‑and‑lodging expenses in addition to the cash scholarship amount [1].

**Summary:** It covers books, equipment and living (board‑and‑lodging) costs.

**pk1r** Tell me the yearly PM Kisan support amount.

The PM‑Kisan scheme provides **Rs 6,000 per year** to each eligible farmer’s family[1].  
**Summary:** Yearly support under PM‑Kisan is Rs 6,000.

**sc1r** Which students qualify for the SC post-matric award?

Students who qualify for the SC post‑matric award are:

* Indian nationals [4]5.1  
* Belong to a Scheduled Caste as determined by the State/UT of domicile [4]5.2  
* Have passed the Matriculation, Higher Secondary or any higher examination of a recognized board or university [4]5.2  
* Have an annual family income of up to Rs 2.50 lakh [5]  
* The scheme gives priority to the poorest households, specifically:  
  – SC households with three or more deprivations under SECC‑2011,  
  – SC households where one or both parents are illiterate, or  
  – SC students who passed 10th standard from a State Government/municipality/local‑body school [5].

**Summary:** SC Indian students with ≤ Rs 2.5 lakh income, proper domicile, required academic qualification, and especially those from the poorest SC households are eligible.

**oos1** What is the PM-KISAN amount in Bangladesh?

I don't know based on the provided documents.

**oos2** How do I apply for PM Awas Yojana?

I don't know based on the provided documents.

**oos3** Who won the 2023 cricket world cup?

I don't know based on the provided documents.

**pk3** Is Aadhaar compulsory to receive PM-KISAN benefits?

Aadhaar is generally required to receive PM‑KISAN benefits. The guidelines state that Aadhaar numbers must be collected for all beneficiaries and that payments from the December 2019‑March 2020 installment onward will be made only through an Aadhaar‑seeded database, with exemptions only for Assam, Meghalaya and Jammu & Kashmir [3]. For the first installment (2018‑19), Aadhaar was mandatory but beneficiaries without it could use other ID proof (e.g., Voter ID) to receive that payment, after which they must enrol in Aadhaar for later installments [5]. The portal lists Aadhaar as an essential farmer attribute, though an Aadhaar enrollment number together with another ID can be used if Aadhaar is not yet available [1].

**Summary:** Aadhaar is compulsory for PM‑KISAN benefits, except for an initial installment using alternate ID and specific state exemptions.

**pk4** How is a family defined under PM-KISAN?

A “farmer’s family” under PM‑KISAN is defined as a family consisting of the husband, wife and minor children that owns cultivable land according to the land records of the relevant State/UT[5].  
**Summary:** The scheme’s family unit is the husband‑wife‑minor‑children household that holds cultivable land.

**jay3** What is the health cover per family per year under PM-JAY?

The Pradhan Mantri Jan Arogya Yojana provides a health‑cover of **₹5 lakh per family per year** on a family‑floater basis[1][3].  

**Summary:** PM‑JAY’s annual benefit for each family is ₹5 lakh.

**sc3** What is the annual parental income limit for the SC post-matric scholarship?

The scheme limits eligibility to students whose parents’/guardians’ total annual income does not exceed **Rs 2,50,000** [2].  

*Summary: The SC post‑matric scholarship’s parental income ceiling is Rs 2.5 lakh per year.*

**sc4** Are students doing correspondence or online courses eligible for the SC post-matric scholarship?

The scholarship guidelines do not mention correspondence or online courses. They only require that the student belong to a Scheduled Caste, be an Indian national, and have passed Matriculation, Higher Secondary or any higher examination of a recognized university or board [4]. No rule is given about the mode of study, so eligibility for correspondence/online courses is not specified in the provided documents.  

**Summary:** The documents do not state whether correspondence or online courses are eligible.

**oos4** What is the PM-JAY health cover in the USA?

I don't know based on the provided documents.

**oos5** Who is the current Agriculture Minister of India?

I don't know based on the provided documents.

**oos6** What will the PM-KISAN installment amount be in 2030?

I don't know based on the provided documents.

## Auto-flagged failure candidates (review these, then write the root cause)

- `pk1`: answerable but the system said 'I don't know'
- `pk1`: expected file `PMKisanSamanNidhi.pdf` not in top-5
- `jay2`: expected file `AMH.pdf` not in top-5
- `sc3`: numbers not found in cited passages: ['2.5']

Known finding: the similarity gate does not separate in-scope from out-of-scope queries (MiniLM scores unrelated questions high), so refusal depends on the LLM prompt.
