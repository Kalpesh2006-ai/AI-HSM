import re
import unicodedata


# ============================================================
# GOVERNMENT SCHEME KEYWORDS
# ============================================================

SCHEME_KEYWORDS = {

    "mudra": [
        # English
        "mudra",
        "pmmy",
        "mudra loan",
        "mudra loans",
        "micro unit development",

        # Hindi
        "मुद्रा",
        "मुद्रा योजना",
        "मुद्रा लोन",
        "मुद्रा ऋण",
        "मुद्रा के तहत",

        # Marathi
        "मुद्रा योजना",
        "मुद्रा कर्ज",
        "मुद्रा ऋण",
        "मुद्रा अंतर्गत",
    ],

    "pmegp": [
        # English
        "pmegp",
        "prime minister employment generation programme",
        "employment generation",
        "kvic",

        # Hindi
        "पीएमईजीपी",
        "पीएमईजीपी योजना",
        "रोजगार सृजन",

        # Marathi
        "रोजगार निर्मिती",
    ],

    "pm_vishwakarma": [
        # English
        "vishwakarma",
        "pm vishwakarma",
        "pm-vishwakarma",
        "artisan",
        "artisans",
        "craftsman",
        "craftsmen",

        # Hindi
        "विश्वकर्मा",
        "पीएम विश्वकर्मा",
        "कारीगर",
        "शिल्पकार",

        # Marathi
        "विश्वकर्मा",
        "कारीगर",
        "कारागीर",
    ],

    "pmfme": [
        # English
        "pmfme",
        "food processing",
        "micro food processing",
        "food processing enterprise",

        # Hindi
        "पीएमएफएमई",
        "खाद्य प्रसंस्करण",
        "खाद्य प्रसंस्करण योजना",

        # Marathi
        "अन्न प्रक्रिया",
        "अन्न प्रक्रिया योजना",
    ],

    "day_nrlm": [
        # English
        "nrlm",
        "day nrlm",
        "self help group",
        "self-help group",
        "shg",
        "rural livelihood",
        "livelihood mission",

        # Hindi
        "डीएवाई एनआरएलएम",
        "दीन दयाल",
        "स्वयं सहायता समूह",
        "सहायता समूह",
        "ग्रामीण आजीविका",

        # Marathi
        "स्वयं सहायता गट",
        "बचत गट",
        "ग्रामीण उपजीविका",
    ],

    "cgtmse": [
        # English
        "cgtmse",
        "credit guarantee",
        "credit guarantee scheme",
        "collateral free",

        # Hindi
        "सीजीटीएमएसई",
        "क्रेडिट गारंटी",
        "बिना जमानत",
        "बिना संपार्श्विक",

        # Marathi
        "क्रेडिट गॅरंटी",
        "तारणाशिवाय",
        "जामीनाशिवाय",
    ],

    "maharashtra_schemes": [
        # English
        "maharashtra scheme",
        "maharashtra schemes",
        "state government scheme",
        "maharashtra government",

        # Hindi
        "महाराष्ट्र योजना",
        "महाराष्ट्र सरकार",
        "महाराष्ट्र सरकारी योजना",

        # Marathi
        "महाराष्ट्र योजना",
        "महाराष्ट्र शासन",
        "महाराष्ट्र सरकारी योजना",
    ],
}


# ============================================================
# GENERAL KNOWLEDGE CATEGORIES
# ============================================================

CATEGORY_KEYWORDS = {

    "entrepreneurship": [

        # English
        "entrepreneurship",
        "entrepreneur",
        "business idea",
        "start a business",
        "starting a business",
        "small business",
        "business planning",
        "business plan",
        "business model",
        "startup",
        "how to start business",
        "business opportunity",

        # Hindi
        "उद्यमिता",
        "उद्यमी",
        "व्यवसाय शुरू",
        "बिजनेस शुरू",
        "व्यवसाय योजना",
        "बिजनेस प्लान",
        "व्यवसाय शुरू करना",
        "छोटा व्यवसाय",

        # Marathi
        "उद्योजकता",
        "उद्योजक",
        "व्यवसाय सुरू",
        "व्यवसाय योजना",
        "बिझनेस सुरू",
        "लघु व्यवसाय",
    ],

    "digital_skills": [

        # English
        "digital skills",
        "smartphone",
        "mobile phone",
        "internet",
        "upi",
        "digital payment",
        "digital payments",
        "online payment",
        "online banking",
        "internet banking",
        "email",
        "government portal",
        "online portal",

        # Hindi
        "डिजिटल कौशल",
        "स्मार्टफोन",
        "मोबाइल",
        "इंटरनेट",
        "यूपीआई",
        "डिजिटल भुगतान",
        "ऑनलाइन भुगतान",
        "ऑनलाइन बैंकिंग",
        "सरकारी पोर्टल",

        # Marathi
        "डिजिटल कौशल्य",
        "स्मार्टफोन",
        "मोबाईल",
        "इंटरनेट",
        "यूपीआय",
        "डिजिटल पेमेंट",
        "ऑनलाईन पेमेंट",
        "ऑनलाईन बँकिंग",
        "सरकारी पोर्टल",
    ],

    "digital_marketing": [

        # English
        "digital marketing",
        "online marketing",
        "social media marketing",
        "whatsapp business",
        "facebook",
        "instagram",
        "social media",
        "online selling",
        "sell online",
        "product promotion",
        "product photography",
        "customer communication",

        # Hindi
        "डिजिटल मार्केटिंग",
        "ऑनलाइन मार्केटिंग",
        "सोशल मीडिया",
        "व्हाट्सएप बिजनेस",
        "ऑनलाइन बिक्री",
        "ऑनलाइन बेचना",
        "उत्पाद प्रचार",
        "ग्राहक संपर्क",

        # Marathi
        "डिजिटल मार्केटिंग",
        "ऑनलाईन मार्केटिंग",
        "सोशल मीडिया",
        "व्हॉट्सअॅप बिझनेस",
        "ऑनलाईन विक्री",
        "उत्पादन प्रचार",
        "ग्राहक संपर्क",
    ],

    "financial_literacy": [

        # English
        "financial literacy",
        "loan",
        "loans",
        "interest",
        "interest rate",
        "emi",
        "bank account",
        "savings",
        "saving",
        "credit",
        "credit score",
        "financial planning",
        "profit",
        "loss",
        "profit and loss",
        "bookkeeping",

        # Hindi
        "वित्तीय साक्षरता",
        "लोन",
        "ऋण",
        "ब्याज",
        "ब्याज दर",
        "ईएमआई",
        "बैंक खाता",
        "बचत",
        "क्रेडिट",
        "वित्तीय योजना",
        "लाभ",
        "हानि",
        "लाभ और हानि",
        "लेखांकन",

        # Marathi
        "आर्थिक साक्षरता",
        "कर्ज",
        "कर्जे",
        "व्याज",
        "व्याज दर",
        "ईएमआय",
        "बँक खाते",
        "बचत",
        "क्रेडिट",
        "आर्थिक नियोजन",
        "नफा",
        "तोटा",
        "नफा आणि तोटा",
        "हिशोब",
    ],

    "business_compliance": [

        # English
        "business compliance",
        "udyam",
        "udyam registration",
        "gst",
        "gst registration",
        "pan card",
        "business license",
        "business licence",
        "license",
        "licence",
        "registration",

        # Hindi
        "व्यवसाय अनुपालन",
        "उद्यम",
        "उद्यम पंजीकरण",
        "जीएसटी",
        "जीएसटी पंजीकरण",
        "पैन कार्ड",
        "व्यवसाय लाइसेंस",
        "पंजीकरण",

        # Marathi
        "व्यवसाय अनुपालन",
        "उद्यम नोंदणी",
        "जीएसटी",
        "जीएसटी नोंदणी",
        "पॅन कार्ड",
        "व्यवसाय परवाना",
        "नोंदणी",
    ],

    "maharashtra": [

        # English
        "maharashtra",
        "maharashtra government",
        "maharashtra women",
        "maharashtra entrepreneur",
        "maharashtra entrepreneurship",
        "self help group maharashtra",
        "rural women maharashtra",

        # Hindi
        "महाराष्ट्र",
        "महाराष्ट्र सरकार",
        "महाराष्ट्र की महिलाएं",
        "महाराष्ट्र उद्यमी",
        "महाराष्ट्र उद्यमिता",
        "महाराष्ट्र स्वयं सहायता समूह",

        # Marathi
        "महाराष्ट्र",
        "महाराष्ट्र शासन",
        "महाराष्ट्र सरकार",
        "महाराष्ट्रातील महिला",
        "महाराष्ट्र उद्योजक",
        "महाराष्ट्र उद्योजकता",
        "महाराष्ट्र बचत गट",
    ],
}


# ============================================================
# TOPIC KEYWORDS
# ============================================================

TOPIC_KEYWORDS = {

    "business_planning": [
        "business plan",
        "business planning",
        "business model",
        "व्यवसाय योजना",
        "बिजनेस प्लान",
        "व्यवसाय नियोजन",
    ],

    "business_ideas": [
        "business idea",
        "business ideas",
        "business opportunity",
        "व्यवसाय विचार",
        "व्यवसाय कल्पना",
        "बिजनेस आइडिया",
        "व्यवसायाची कल्पना",
    ],

    "digital_payments": [
        "upi",
        "digital payment",
        "digital payments",
        "online payment",
        "यूपीआई",
        "डिजिटल भुगतान",
        "ऑनलाइन भुगतान",
        "डिजिटल पेमेंट",
        "ऑनलाईन पेमेंट",
    ],

    "whatsapp_business": [
        "whatsapp business",
        "व्हाट्सएप बिजनेस",
        "व्हॉट्सअॅप बिझनेस",
    ],

    "online_selling": [
        "online selling",
        "sell online",
        "selling online",
        "ऑनलाइन बिक्री",
        "ऑनलाइन बेचना",
        "ऑनलाईन विक्री",
    ],

    "loans": [
        "loan",
        "loans",
        "लोन",
        "ऋण",
        "कर्ज",
    ],

    "emi": [
        "emi",
        "ईएमआई",
        "ईएमआय",
    ],

    "profit_loss": [
        "profit",
        "loss",
        "profit and loss",
        "लाभ",
        "हानि",
        "लाभ और हानि",
        "नफा",
        "तोटा",
        "नफा आणि तोटा",
    ],

    "udyam_registration": [
        "udyam",
        "udyam registration",
        "उद्यम",
        "उद्यम पंजीकरण",
        "उद्यम नोंदणी",
    ],

    "gst": [
        "gst",
        "gst registration",
        "जीएसटी",
        "जीएसटी पंजीकरण",
        "जीएसटी नोंदणी",
    ],
}


# ============================================================
# WOMEN-RELATED TERMS
# ============================================================

WOMEN_TERMS = [

    # English
    "women",
    "woman",
    "female",
    "women entrepreneur",
    "women entrepreneurs",
    "female entrepreneur",
    "female entrepreneurs",
    "women beneficiaries",

    # Hindi
    "महिला",
    "महिलाएं",
    "महिलाओं",
    "महिला उद्यमी",
    "महिला उद्यमियों",
    "महिला लाभार्थी",

    # Marathi
    "महिला",
    "महिलांना",
    "महिलांसाठी",
    "महिला उद्योजक",
    "महिला उद्योजिका",
    "महिला लाभार्थी",
]


# ============================================================
# NORMALIZATION
# ============================================================

def normalize_query(query):
    """
    Normalize the user's question while preserving
    Hindi, Marathi, English and other Unicode characters.
    """

    query = query.lower().strip()

    cleaned_chars = []

    for char in query:

        category = unicodedata.category(char)

        if (
            category.startswith("L")
            or category.startswith("N")
            or category.startswith("M")
            or char.isspace()
            or char == "-"
        ):
            cleaned_chars.append(char)

        else:
            cleaned_chars.append(" ")

    query = "".join(cleaned_chars)

    query = " ".join(query.split())

    return query.strip()


# ============================================================
# DETECT GOVERNMENT SCHEMES
# ============================================================

def detect_scheme(query):

    normalized_query = normalize_query(query)

    detected_schemes = []

    for scheme, keywords in SCHEME_KEYWORDS.items():

        for keyword in keywords:

            keyword_normalized = normalize_query(
                keyword
            )

            if keyword_normalized in normalized_query:

                detected_schemes.append(scheme)

                break

    return detected_schemes


# ============================================================
# DETECT GENERAL CATEGORIES
# ============================================================

def detect_categories(query):

    normalized_query = normalize_query(query)

    detected_categories = []

    for category, keywords in CATEGORY_KEYWORDS.items():

        for keyword in keywords:

            keyword_normalized = normalize_query(
                keyword
            )

            if keyword_normalized in normalized_query:

                detected_categories.append(category)

                break

    return detected_categories


# ============================================================
# DETECT TOPICS
# ============================================================

def detect_topics(query):

    normalized_query = normalize_query(query)

    detected_topics = []

    for topic, keywords in TOPIC_KEYWORDS.items():

        for keyword in keywords:

            keyword_normalized = normalize_query(
                keyword
            )

            if keyword_normalized in normalized_query:

                detected_topics.append(topic)

                break

    return detected_topics


# ============================================================
# DETECT WOMEN-RELATED QUESTIONS
# ============================================================

def is_women_related(query):

    normalized_query = normalize_query(query)

    for term in WOMEN_TERMS:

        term_normalized = normalize_query(term)

        if term_normalized in normalized_query:

            return True

    return False


# ============================================================
# QUERY EXPANSION
# ============================================================

def expand_query(query):

    normalized_query = normalize_query(query)

    schemes = detect_scheme(query)

    categories = detect_categories(query)

    topics = detect_topics(query)

    expanded_queries = []

    # Always keep original question
    expanded_queries.append(query)

    # ========================================================
    # MUDRA
    # ========================================================

    if "mudra" in schemes:

        expanded_queries.extend([
            "MUDRA PMMY loan eligibility",
            "MUDRA PMMY women entrepreneurs",
            "MUDRA women beneficiaries",
            "women entrepreneurs PMMY MUDRA loans",
            "female entrepreneurs MUDRA",
            "68% PMMY loans women entrepreneurs",

            "महिलाओं को मुद्रा योजना के तहत लोन",
            "महिलाओं के लिए मुद्रा योजना",
            "महिला उद्यमी मुद्रा योजना",
            "महिला मुद्रा लोन पात्रता",
            "महिला मुद्रा योजना ऋण",
            "मुद्रा योजना महिला लाभार्थी",

            "महिलांना मुद्रा योजनेअंतर्गत कर्ज",
            "महिलांसाठी मुद्रा योजना",
            "महिला उद्योजक मुद्रा योजना",
            "महिला मुद्रा कर्ज पात्रता",
            "मुद्रा योजना महिला लाभार्थी",

            "68% PMMY loans women entrepreneurs",
        ])

    # ========================================================
    # PMEGP
    # ========================================================

    if "pmegp" in schemes:

        expanded_queries.extend([
            "PMEGP eligibility",
            "PMEGP women entrepreneurs",
            "PMEGP special category women",
            "PMEGP subsidy rural women",
            "PMEGP beneficiary contribution women",
        ])

    # ========================================================
    # PM VISHWAKARMA
    # ========================================================

    if "pm_vishwakarma" in schemes:

        expanded_queries.extend([
            "PM Vishwakarma eligibility",
            "PM Vishwakarma women artisans",
            "PM Vishwakarma benefits",
            "PM Vishwakarma loan",
            "PM Vishwakarma government scheme",
        ])

    # ========================================================
    # PMFME
    # ========================================================

    if "pmfme" in schemes:

        expanded_queries.extend([
            "PMFME eligibility",
            "PMFME women entrepreneurs",
            "PMFME food processing benefits",
            "PMFME financial assistance",
            "PMFME micro food processing enterprises",
        ])

    # ========================================================
    # DAY-NRLM
    # ========================================================

    if "day_nrlm" in schemes:

        expanded_queries.extend([
            "DAY NRLM women",
            "DAY NRLM self help groups",
            "DAY NRLM women entrepreneurs",
            "DAY NRLM rural women livelihood",
            "DAY NRLM benefits",
        ])

    # ========================================================
    # CGTMSE
    # ========================================================

    if "cgtmse" in schemes:

        expanded_queries.extend([
            "CGTMSE eligibility",
            "CGTMSE women entrepreneurs",
            "CGTMSE credit guarantee",
            "CGTMSE collateral free loan",
            "CGTMSE benefits",
        ])

    # ========================================================
    # MAHARASHTRA GOVERNMENT SCHEMES
    # ========================================================

    if "maharashtra_schemes" in schemes:

        expanded_queries.extend([
            "Maharashtra government schemes women entrepreneurs",
            "Maharashtra women entrepreneurship scheme",
            "Maharashtra government entrepreneurship benefits",
        ])

    # ========================================================
    # GENERAL KNOWLEDGE EXPANSION
    #
    # If a specific government scheme is detected,
    # scheme-specific retrieval gets priority.
    #
    # This prevents questions about MUDRA, PMEGP, etc.
    # from being diluted by unrelated generic searches.
    #
    # If no specific scheme is detected, multiple
    # knowledge categories can work together.
    # ========================================================

    if not schemes:

        # ----------------------------------------------------
        # ENTREPRENEURSHIP
        # ----------------------------------------------------

        if "entrepreneurship" in categories:

            expanded_queries.extend([
                "how to start a small business",
                "entrepreneurship basics",
                "small business planning",
                "business planning for women entrepreneurs",
                "starting a rural business",
            ])

        # ----------------------------------------------------
        # DIGITAL SKILLS
        # ----------------------------------------------------

        if "digital_skills" in categories:

            expanded_queries.extend([
                "digital skills for women entrepreneurs",
                "smartphone basics",
                "internet basics",
                "digital payments",
                "online banking",
                "government online portals",
            ])

        # ----------------------------------------------------
        # DIGITAL MARKETING
        # ----------------------------------------------------

        if "digital_marketing" in categories:

            expanded_queries.extend([
                "digital marketing for small business",
                "WhatsApp Business for entrepreneurs",
                "social media marketing for small business",
                "online selling",
                "product promotion",
                "customer communication",
            ])

        # ----------------------------------------------------
        # FINANCIAL LITERACY
        # ----------------------------------------------------

        if "financial_literacy" in categories:

            expanded_queries.extend([
                "financial literacy for entrepreneurs",
                "business loans",
                "interest rates",
                "EMI",
                "bank accounts",
                "savings",
                "credit",
                "basic financial planning",
            ])

        # ----------------------------------------------------
        # BUSINESS COMPLIANCE
        # ----------------------------------------------------

        if "business_compliance" in categories:

            expanded_queries.extend([
                "Udyam registration",
                "GST registration",
                "PAN for business",
                "business licences",
                "business registration requirements",
            ])

        # ----------------------------------------------------
        # MAHARASHTRA
        # ----------------------------------------------------

        if "maharashtra" in categories:

            expanded_queries.extend([
                "Maharashtra women entrepreneurs",
                "Maharashtra rural entrepreneurship",
                "Maharashtra women entrepreneurship support",
                "Maharashtra self help groups",
            ])

        # ----------------------------------------------------
        # TOPIC-SPECIFIC EXPANSION
        # ----------------------------------------------------

        if "business_planning" in topics:

            expanded_queries.extend([
                "how to create a business plan",
                "small business planning",
                "business plan for rural women",
            ])

        if "business_ideas" in topics:

            expanded_queries.extend([
                "small business ideas",
                "rural business ideas",
                "business opportunities for women",
            ])

        if "digital_payments" in topics:

            expanded_queries.extend([
                "how to use UPI",
                "how to make digital payments",
                "UPI for small business",
            ])

        if "whatsapp_business" in topics:

            expanded_queries.extend([
                "how to use WhatsApp Business",
                "WhatsApp Business for selling products",
            ])

        if "online_selling" in topics:

            expanded_queries.extend([
                "how to sell products online",
                "online selling for small business",
            ])

        if "loans" in topics:

            expanded_queries.extend([
                "business loan",
                "small business loan",
                "loan for women entrepreneurs",
            ])

        if "emi" in topics:

            expanded_queries.extend([
                "what is EMI",
                "loan EMI explanation",
                "EMI calculation basics",
            ])

        if "profit_loss" in topics:

            expanded_queries.extend([
                "profit and loss for small business",
                "how to calculate business profit",
                "basic bookkeeping",
            ])

        if "udyam_registration" in topics:

            expanded_queries.extend([
                "Udyam registration for small business",
                "how to register Udyam",
            ])

        if "gst" in topics:

            expanded_queries.extend([
                "GST registration for small business",
                "GST basics for entrepreneurs",
            ])


    # ========================================================
    # REMOVE DUPLICATES
    # ========================================================

    unique_queries = []

    seen = set()

    for q in expanded_queries:

        normalized_q = normalize_query(q)

        if normalized_q not in seen:

            seen.add(normalized_q)

            unique_queries.append(q)

    return {
        "original_query": query,
        "normalized_query": normalized_query,

        "detected_schemes": schemes,

        "detected_categories": categories,

        "detected_topics": topics,

        "women_related": is_women_related(query),

        "expanded_queries": unique_queries,
    }


# ============================================================
# MAIN QUERY ROUTER
# ============================================================

def route_query(query):

    result = expand_query(query)

    return result


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print("======================================")
    print("AI-HSM Query Router Test")
    print("======================================")

    question = input("\nEnter your question: ")

    result = route_query(question)

    print("\nOriginal Question:")
    print(result["original_query"])

    print("\nNormalized Question:")
    print(result["normalized_query"])

    print("\nDetected Schemes:")

    if result["detected_schemes"]:

        for scheme in result["detected_schemes"]:
            print(f"- {scheme}")

    else:
        print("- No specific scheme detected")

    print("\nDetected Categories:")

    if result["detected_categories"]:

        for category in result["detected_categories"]:
            print(f"- {category}")

    else:
        print("- No specific category detected")

    print("\nDetected Topics:")

    if result["detected_topics"]:

        for topic in result["detected_topics"]:
            print(f"- {topic}")

    else:
        print("- No specific topic detected")

    print("\nWomen Related:")
    print(result["women_related"])

    print("\nExpanded Search Queries:")

    for i, search_query in enumerate(
        result["expanded_queries"],
        start=1
    ):

        print(f"{i}. {search_query}")