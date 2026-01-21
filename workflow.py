#Importing dependencies 
from openai import OpenAI
import json
import requests
import datetime as dt
import base64, os 
from email.message import EmailMessage
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Defining Functions
def convert_abstract_to_text(dict_1):
    word_count = 0 
    for key in dict_1.keys():
        word_count += len(dict_1[key])
    abstract_list = [''] * word_count
    for key in dict_1.keys():
        for index in dict_1[key]:
            abstract_list[index] = key
    abstract = ' '.join(abstract_list)
    return abstract


# Base URL for OpenAlex "works" API
BASE_URL = "https://api.openalex.org/works"

#Taking professor name, generating paper title and abstract in a dictionary  
professor_name = "Edoardo Albisetti"

author_resp = requests.get("https://api.openalex.org/authors", params={"search": professor_name})
author_data = author_resp.json()
author_id = author_data['results'][0]['id']

from_date = (dt.date.today() - dt.timedelta(days=730)).isoformat()
params={
        "filter": f"author.id:{author_id},from_publication_date:{from_date}",
        "sort": "publication_date:desc",   
    }
response = requests.get(BASE_URL, params=params)
data = response.json()

papers_dict = {}

for i in range(len(data['results'])):
    try:
        papers_dict[data['results'][i]['title']] = convert_abstract_to_text(data['results'][i]['abstract_inverted_index'])
    except:
        papers_dict[data['results'][i]['title']] = ""

# Storing necessary information for email generation 
email_examples = f"""
1. Dear Professor Ielmini,
I hope this message finds you well. My name is Aashman Mehta, and I’m a sophomore physics major at UCLA with a strong interest in neuromorphic and physics-inspired computing hardware and architecture.
I recently came across your paper on the fully integrated analogue closed-loop in-memory computing accelerator and found it extremely
fascinating. I would love to learn about your work, especially on this chip.
I would really appreciate the opportunity to connect with you for 15 minutes over an online meeting, according to your convenience to learn about your work and the field in general. Thank you so much for your time and consideration
Best,
Aashman


3. Dear Professor Narang,
My name is Aashman Mehta, and I am an undergraduate at UCLA majoring in Physics and Computer Science. 
I am extremely fascinated by your group’s work on quantum materials for hosting qubits—such as your first-principles studies of moiré superlattices in twisted bilayer systems—which highlight the potential of atom-like quantum wells for scalable quantum architectures. I was also excited to read about your exploration of low-dimensional magnetism in van der Waals compounds and its implications for quantum sensing.
I would be very grateful for the opportunity to contribute to your group’s efforts, and would love the chance to briefly meet with you or a lab member to learn more about potential opportunities.  
I have attached my resume for your reference. Thank you very much for your time and consideration.
Best regards,
Aashman Mehta  

4. Dear Professor Wong 
I hope this message finds you well. My name is Aashman Mehta, and I’m an undergraduate physics and computer science major at UCLA with a strong interest in hardware development for artificial intelligence and quantum computing. 
I read about your work on Superconducting qubits and microprocessors and found it extremely interesting, especially your recent work on quantum gate teleportation using photonic chips. 
I am writing to inquire about potential internship opportunities at your lab. I am eager to work in any opportunity where I can develop research skills, and I promise to dedicate time and effort.
I’ve attached my resume for your review and would greatly appreciate the chance to discuss any internship opportunities.
Thank you for your time and consideration. I look forward to hearing from you.
Best regards,
Aashman Mehta

5. Dear Professor Iyer
I hope this message finds you well. My name is Aashman Mehta, and I’m an undergraduate physics and materials sciences major at UCLA with a strong interest in semiconductor research.
I recently read your paper on pulsed flash boiling for high heat flux electronics cooling, and I found it incredibly compelling — especially the system's ability to recover from dry-out conditions. I’m deeply interested in learning more about this work and its broader implications for thermal management in advanced electronic systems.
I would love to learn more about the research. I am writing to inquire about potential internship opportunities at your lab. I am eager to work in any opportunity where I can develop research skills, and I promise to dedicate time and effort. I’ve attached my resume for your review and would greatly appreciate the chance to discuss any internship opportunities.
Thank you for your time and consideration. I look forward to hearing from you.
Best regards,
Aashman Mehta

6. Dear Dr. Saha
I hope this message finds you well. My name is Aashman Mehta, and I’m an undergraduate physics and materials sciences major at UCLA with a strong interest in magnetic materials.
I recently read your work on constructing logic gates and computation circuits using magnetic skyrmions and found it incredibly interesting, especially your analysis of how skyrmions interact using micromagnetic simulation.
I am writing to inquire about potential internship opportunities at your lab for the summer. I am eager to work in any opportunity where I can develop research skills, and I promise to dedicate time and effort.
I’ve attached my resume for your review and would greatly appreciate the chance to discuss any internship opportunities.
Thank you for your time and consideration. I look forward to hearing from you.
Best regards,
Aashman Mehta"""

resume_text = """RESEARCH INTERESTS 
Low-dimensional quantum materials (strongly correlated and topological systems), nanoscale device physics and electronic transport; physics-based and neuromorphic computing architectures enabled by spintronic, photonic, and low dimensional material platforms; post-CMOS and hybrid CMOS-compatible systems.
 
EDUCATION  
University of California, Los Angeles (UCLA)					                                         Graduation Expected June 2028
B.S. Physics	 				                                                                                                                                           GPA 3.891
Honors: Dean’s list for (4 quarters), Honors Student in Physics
Relevant Coursework: Electromagnetism, Upper Division Linear Algebra, Analog & Digital Circuit Design and Instrumentation, Data Structures and Algorithms, Discrete Mathematics

TECHNICAL SKILLS 
 
Machine Learning: supervised learning (regression, classification); feedforward and recurrent neural networks; oscillator- and reservoir-inspired architectures
Programming: Python (data analysis, multi-instrument control, automated data acquisition, API integration), C++, SQL, R
Modeling & Simulation: MATLAB, MuMax3 (micromagnetics), COMSOL Multiphysics (numerical modeling of coupled physical systems)
CAD: KLayout (lithographic layout design)
Device Fabrication & Characterization: nanoscale device design and lithography; fabrication of layered low-dimensional material heterostructures; electrical transport measurements (I–V, illumination- and field-dependent characterization)

RESEARCH EXPERIENCE
 
Balandin Group - UCLA					                					Los Angeles, USA
Undergraduate Researcher | Dept. of Materials Science and Engineering					    September 2025 – Present
•	Designed and fabricated nanoscale TaS₂/hBN heterostructure devices on SiO₂ substrates with lithographically defined electrodes for electrical transport studies.
•	Developed custom Hall-bar and multi-terminal (4–8 terminal) device geometries in KLayout to enable laser-based patterning as an alternative to electron-beam lithography, reducing cleanroom time and fabrication costs while improving fabrication throughput.
•	Fabricating and characterizing strongly correlated-electron devices based on charge-density-wave (CDW) materials for quantum oscillator network studies.
•	Investigating photo-responsive and phase-dependent transport phenomena in low-dimensional materials relevant to co-designed sensing and computing architectures.

Department of Physics - Ashoka University 									       Sonepat, India
Summer Research Intern | Dr. Susmita Saha                           					                                      May 2025 – August 2025
•	Contributed to the conceptual design of a reservoir computing architecture exploiting nonlinear and anisotropic interactions between spin waves and skyrmions.
•	Modeled spin-wave modes and skyrmion dynamics in ferromagnetic nanostructures using micromagnetic simulations (MuMax3).
•	Analyzed nonlinear spin-wave propagation and skyrmion behavior via simulated ferromagnetic resonance (FMR) and spin-wave spectroscopy.
•	Integrated simulated spin-wave responses into a machine-learning framework to realize neuromorphic computing primitives.
•	Evaluated reservoir stability, memory capacity, and nonlinearity using parameter sweeps 
•	Benchmarking computational performance on standard reservoir computing tasks, including Mackey–Glass chaotic time-series prediction, and spoken-digit recognition.
•	Delivered an end-of-internship research presentation to the Department of Physics, Ashoka University.

Basic Plasma Science Facility (BaPSF), University of California – Los Angeles					 Los Angeles, USA
Project Intern with Dr. Walter Gekelman					        			                      April 2025 – August 2025
•	Developed a Python-based automation framework for synchronized multi-instrument control in plasma etching experiments.
•	Implemented automated data acquisition, real-time analysis, and visualization pipelines to improve experimental throughput and reproducibility.

PROJECTS
 
AI-Powered Personalized Outreach Automation 
•	Designed an end-to-end Python pipeline integrating OpenAlex and Gmail APIs to analyze research profiles and generate personalized outreach.
•	Implemented relevance scoring and automated drafting, reducing outreach time by 83% and achieving a 25% positive response rate across 100+ emails

Machine Learning-Enabled Optimization of Controlled-Release Fertilizers Using Bio-Based Hydrogels  
•	Characterized water absorption behavior in hydrogels synthesized from different biodegradable polymer systems.
•	Modeled nutrient release dynamics from fertilizer-loaded biodegradable hydrogels under varying environmental conditions.
•	Trained supervised learning models (XGBoost), incorporating feature engineering and cross-validation, to optimize fertilizer–hydrogel combinations.
"""

#Using list of works of the professor to generate email using chatgpt api
prompt_string = f"""I will provide:
1. The professor’s name
2. Their  most recent papers (title + abstract/summary)
3. A list of my interests and resume highlights
4. Examples of cold emails I have written bere as a sample

Your task:
- Pick the 1–2 papers most relevant to me, based on the list of fields I am interested in and my resume
- Draft a cold email to the professor in the style of my examples, where you introduce me, explain my interest in their research, and express an interest in connecting with them over a potential meeting for 15 minutes.
- Keep the structure and tone consistent with the examples, and make sure everything gels well.
- Keep length <120 words.
- Include a subject line upfront (5–8 words) in the format: Inquiry about (Qubit Modeling – or whatever their research is on) Research.
- Include the subject line before the email. Do NOT write "Subject:". After the subject line, insert a '\\n' character to separate it from the email.
- Begin the email with the remarks: Dear Professor (Professor's last name),
- Always begin with: "I hope this message finds you well. My name is Aashman Mehta, and I’m a sophomore physics major at UCLA with a strong interest in physics-inspired computing hardware and architecture."
    - Do not add unnecessary modifiers beyond this broad field.
- Then, say that I read his paper or came across his work on ____ and found ___ it very interesting - give a genuine compliment that sounds like I read it. Don't mention the title of the paper and quote from there. Rather, mention I read about this work and found XYZ very interesting. The compliment should look like I read the paper and I am mostly just very inquisitive to learn about how the technoogy they developed works. Keep this mention and compliment combined 30-50 words and make it
look like an inquisitive guy who wants to know about the work
- Then very naturally connect this with the idea that I want to have a quick online meeting with them to learn about their work. 
- Make small paragraphs, rather than a single block of text and ensure the email sounds genuine curiosity by someone who is interested in the field even though not as knowledgeable as a PhD student.
- Output only the email text (no preamble, no explanation).
- You can rephrase my points so that it flows like a conversation, and sounds genuine curiosity and interest in the field.
- While the entire email should sound like a single cohesive piece and a conversation, it should still be written formally. 
- The email body content should be stricltly less than 150 words. 
- I want to demonstrate strong passionfor their work, strong curiosity, and the email should ideally be asking for an opportunity to learn more about a specific part of their research. and in the end it should say, I would also like to discuss any opportunities where I can contribute. 
- While learning from the given email examples, give strong preference to the tone and structure of email 1, while also learning from the rest just as well. 
- Always end by thanking them for their time and consideration and with salutations 
- Format it like a normal email don't have randomly formatted email with randomly placed endlines

Professor's name: {professor_name}

The professor's most recent papers: {papers_dict}

A list with fields of my interest : [physical reservoir computing, reservoir computing, machine learning, neuromorphic computing, neural networks, chip design, CMOS, wafer-scale building, semiconductor design, qubits,  AI hardware, robotics, autonomous vehicles, wearable electronics, quantum computing, qubits, superconducting qubits, spin qubits, trapped-ion qubits, quantum microprocessors, quantum algorithms, quantum error correction, quantum communication, quantum simulation, quantum optics, photonics, cavity QED, circuit QED, quantum sensing, quantum metrology, quantum materials, magnetic materials, spintronics, skyrmions, spin waves, multiferroics, superconductors, high-temperature superconductors, green superconductors, strongly correlated materials, topological materials, low-dimensional materials, metamaterials, defect engineering in materials, amorphous and glassy materials, plasma physics, fusion energy, magnetohydrodynamics, laser–plasma interactions, space plasmas, control theory and dynamical systems (applied to physics and engineering), embedded systems for AI and quantum control, sustainable energy materials, photovoltaics, perovskite solar cells, thin-film solar cells, multi-junction solar cells, battery materials (Li-ion, Na-ion, Mg-ion, Ca-ion, solid-state electrolytes), supercapacitors, hybrid energy storage, fuel cells, solid oxide fuel cells, hydrogen storage, ammonia storage, catalysts for hydrogen evolution, oxygen reduction, and CO₂ reduction, thermoelectric materials, waste-heat recovery materials, piezoelectric and triboelectric energy harvesters, phase-change and thermal energy storage materials]

Example of emails that I have written before: {email_examples}

"""

client = OpenAI(client = OpenAI(api_key=os.environ["OPENAI_API_KEY"]))

response = client.chat.completions.create(
  model="gpt-5-nano",
  messages=[{"role": "system", "content": "You are a cold mailing and networking expert and are helping me write tailored cold emails to professors."},
            {"role": "user", "content": prompt_string}]
)
data = response.model_dump()

text = data['choices'][0]['message']['content']
subject = text.split('\n')[0]
email_text = text[len(subject)+1:]
print(subject)
print("\n\n\n\n")
print(email_text)

# ---------------------------------------------------- CONFIG -----------------------------------------------------
scopes = ["https://www.googleapis.com/auth/gmail.compose"]
to = "a406467467@gmail.com"
resume_path = "replace_resume.pdf"


# OAuth for Gmail
def gmail_service():
    # First time: place Google OAuth client_secret.json in working dir
    flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", scopes=scopes)
    creds = flow.run_local_server(port=0)
    return build("gmail", "v1", credentials=creds)

# Build MIME message with attachment
def build_message(to, subject, body, attachment_path):
    msg = EmailMessage()
    msg["To"] = to
    msg["Subject"] = subject
    msg["From"] = "me"   # Gmail API replaces 'me' on send/draft
    msg.set_content(body)
    with open(attachment_path, "rb") as f:
        data = f.read()
    msg.add_attachment(data, maintype="application", subtype="pdf", filename=os.path.basename(attachment_path))
    return msg

# Create Gmail draft
def create_draft(service, message):
    encoded = base64.urlsafe_b64encode(message.as_bytes()).decode()
    draft = {"message": {"raw": encoded}}
    return service.users().drafts().create(userId="me", body=draft).execute()
    
if __name__ == "__main__":
    mime = build_message(to, subject, email_text)
    svc = gmail_service()
    draft = create_draft(svc, mime)
    print("Draft created with ID:", draft.get("id"))
