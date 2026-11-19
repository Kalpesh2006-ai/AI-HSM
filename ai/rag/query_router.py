
import re
import unicodedata


# ============================================================
# GOVERNMENT SCHEME KEYWORDS
# ============================================================

SCHEME_KEYWORDS = {
    "mudra": [
        "mudra", "pmmy", "mudra loan", "mudra loans",
        "micro unit development",
        "मुद्रा", "मुद्रा योजना", "मुद्रा लोन", "मुद्रा ऋण",
        "मुद्रा के तहत", "मुद्रा कर्ज", "मुद्रा अंतर्गत",
    ],

    "pmegp": [
        "pmegp",
        "prime minister employment generation programme",
        "prime minister employment generation program",
        "employment generation", "kvic",
        "पीएमईजीपी", "पीएमईजीपी योजना", "रोजगार सृजन",
        "प्रधानमंत्री रोजगार सृजन",
        "प्रधानमंत्री रोजगार सृजन कार्यक्रम",
        "रोजगार निर्मिती",
        # Common Whisper transcription variations
        "रूस्गास विजन कारिक्रम",
        "रोजगार विजन कार्यक्रम",
        "रोजगार सृजन कारिक्रम",
        "रोजगार जनरेशन",
    ],

    "pm_vishwakarma": [
        "vishwakarma", "pm vishwakarma", "pm-vishwakarma",
        "artisan", "artisans", "craftsman", "craftsmen",
        "विश्वकर्मा", "विश्वकर्म", "पीएम विश्वकर्मा",
        "प्रधानमंत्री विश्वकर्मा", "प्रधानमंत्री विश्वकर्म",
        "कारीगर", "शिल्पकार",
        "विश्वकर्मा योजना", "विश्वकर्म योजना",
        "कारागीर",
    ],

    "pmfme": [
        "pmfme", "food processing", "micro food processing",
        "food processing enterprise",
        "पीएमएफएमई", "खाद्य प्रसंस्करण",
        "खाद्य प्रसंस्करण योजना",
        "अन्न प्रक्रिया", "अन्न प्रक्रिया योजना",
    ],

    "day_nrlm": [
        "nrlm", "day nrlm", "self help group",
        "self-help group", "shg", "rural livelihood",
        "livelihood mission",
        "डीएवाई एनआरएलएम", "दीन दयाल",
        "स्वयं सहायता समूह", "सहायता समूह",
        "ग्रामीण आजीविका",
        "स्वयं सहायता गट", "बचत गट",
        "ग्रामीण उपजीविका",
    ],

    "cgtmse": [
        "cgtmse", "credit guarantee",
        "credit guarantee scheme", "collateral free",
        "सीजीटीएमएसई", "क्रेडिट गारंटी",
        "बिना जमानत", "बिना संपार्श्विक",
        "क्रेडिट गॅरंटी", "तारणाशिवाय",
        "जामीनाशिवाय",
    ],

    "maharashtra_schemes": [
        "maharashtra scheme", "maharashtra schemes",
        "state government scheme", "maharashtra government",
        "महाराष्ट्र योजना", "महाराष्ट्र सरकार",
        "महाराष्ट्र सरकारी योजना", "महाराष्ट्र शासन",
    ],
}


# ============================================================
# GENERAL KNOWLEDGE CATEGORIES
# ============================================================

CATEGORY_KEYWORDS = {
    "entrepreneurship": [
        "entrepreneurship", "entrepreneur", "business idea",
        "start a business", "starting a business",
        "small business", "business planning", "business plan",
        "business model", "startup", "how to start business",
        "business opportunity",
        "उद्यमिता", "उद्यमी", "व्यवसाय शुरू",
        "बिजनेस शुरू", "व्यवसाय योजना", "बिजनेस प्लान",
        "व्यवसाय शुरू करना", "छोटा व्यवसाय",
        "उद्योजकता", "उद्योजक", "व्यवसाय सुरू",
        "व्यवसाय योजना", "बिझनेस सुरू", "लघु व्यवसाय",
    ],

    "digital_skills": [
        "digital skills", "smartphone", "mobile phone",
        "internet", "upi", "digital payment",
        "digital payments", "online payment", "online banking",
        "internet banking", "email", "government portal",
        "online portal",
        "डिजिटल कौशल", "स्मार्टफोन", "मोबाइल",
        "इंटरनेट", "यूपीआई", "डिजिटल भुगतान",
        "ऑनलाइन भुगतान", "ऑनलाइन बैंकिंग", "सरकारी पोर्टल",
        "डिजिटल कौशल्य", "मोबाईल", "यूपीआय",
        "डिजिटल पेमेंट", "ऑनलाईन पेमेंट",
        "ऑनलाईन बँकिंग", "सरकारी पोर्टल",
    ],

    "digital_marketing": [
        "digital marketing", "online marketing",
        "social media marketing", "whatsapp business",
        "facebook", "instagram", "social media",
        "online selling", "sell online", "product promotion",
        "product photography", "customer communication",
        "डिजिटल मार्केटिंग", "ऑनलाइन मार्केटिंग",
        "सोशल मीडिया", "व्हाट्सएप बिजनेस",
        "ऑनलाइन बिक्री", "ऑनलाइन बेचना",
        "उत्पाद प्रचार", "ग्राहक संपर्क",
        "ऑनलाईन मार्केटिंग", "व्हॉट्सअॅप बिझनेस",
        "ऑनलाईन विक्री", "उत्पादन प्रचार",
    ],

    "financial_literacy": [
        "financial literacy", "loan", "loans", "interest",
        "interest rate", "emi", "bank account", "savings",
        "saving", "credit", "credit score", "financial planning",
        "profit", "loss", "profit and loss", "bookkeeping",
        "वित्तीय साक्षरता", "लोन", "ऋण", "ब्याज",
        "ब्याज दर", "ईएमआई", "बैंक खाता", "बचत",
        "क्रेडिट", "वित्तीय योजना", "लाभ", "हानि",
        "लाभ और हानि", "लेखांकन",
        "आर्थिक साक्षरता", "कर्ज", "कर्जे", "व्याज",
        "व्याज दर", "ईएमआय", "बँक खाते",
        "आर्थिक नियोजन", "नफा", "तोटा", "हिशोब",
    ],

    "business_compliance": [
        "business compliance", "udyam", "udyam registration",
        "gst", "gst registration", "pan card",
        "business license", "business licence",
        "license", "licence", "registration",
        "व्यवसाय अनुपालन", "उद्यम", "उद्यम पंजीकरण",
        "जीएसटी", "जीएसटी पंजीकरण", "पैन कार्ड",
        "व्यवसाय लाइसेंस", "पंजीकरण",
        "उद्यम नोंदणी", "जीएसटी नोंदणी",
        "पॅन कार्ड", "व्यवसाय परवाना", "नोंदणी",
    ],

    "maharashtra": [
        "maharashtra", "maharashtra government",
        "maharashtra women", "maharashtra entrepreneur",
        "maharashtra entrepreneurship",
        "self help group maharashtra",
        "rural women maharashtra",
        "महाराष्ट्र", "महाराष्ट्र सरकार",
        "महाराष्ट्र की महिलाएं", "महाराष्ट्र उद्यमी",
        "महाराष्ट्र उद्यमिता", "महाराष्ट्र स्वयं सहायता समूह",
        "महाराष्ट्र शासन", "महाराष्ट्रातील महिला",
        "महाराष्ट्र उद्योजक", "महाराष्ट्र उद्योजकता",
        "महाराष्ट्र बचत गट",
    ],
}


# ============================================================
# TOPIC KEYWORDS
# ============================================================

TOPIC_KEYWORDS = {
    "business_planning": [
        "business plan", "business planning", "business model",
        "व्यवसाय योजना", "बिजनेस प्लान", "व्यवसाय नियोजन",
    ],

    "business_ideas": [
        "business idea", "business ideas", "business opportunity",
        "व्यवसाय विचार", "व्यवसाय कल्पना", "बिजनेस आइडिया",
        "व्यवसायाची कल्पना",
    ],

    "digital_payments": [
        "upi", "digital payment", "digital payments",
        "online payment", "यूपीआई", "डिजिटल भुगतान",
        "ऑनलाइन भुगतान", "डिजिटल पेमेंट", "ऑनलाईन पेमेंट",
    ],

    "whatsapp_business": [
        "whatsapp business", "व्हाट्सएप बिजनेस",
        "व्हॉट्सअॅप बिझनेस",
    ],

    "online_selling": [
        "online selling", "sell online", "selling online",
        "ऑनलाइन बिक्री", "ऑनलाइन बेचना", "ऑनलाईन विक्री",
    ],

    "loans": [
        "loan", "loans", "लोन", "ऋण", "कर्ज",
    ],

    "emi": [
        "emi", "ईएमआई", "ईएमआय",
    ],

    "profit_loss": [
        "profit", "loss", "profit and loss",
        "लाभ", "हानि", "लाभ और हानि",
        "नफा", "तोटा", "नफा आणि तोटा",
    ],

    "udyam_registration": [
        "udyam", "udyam registration",
        "उद्यम", "उद्यम पंजीकरण", "उद्यम नोंदणी",
    ],

    "gst": [
        "gst", "gst registration", "जीएसटी",
        "जीएसटी पंजीकरण", "जीएसटी नोंदणी",
    ],
}


# ============================================================
# WOMEN-RELATED TERMS
# ============================================================

WOMEN_TERMS = [
    "women", "woman", "female",
    "women entrepreneur", "women entrepreneurs",
    "female entrepreneur", "female entrepreneurs",
    "women beneficiaries",
    "महिला", "महिलाएं", "महिलाओं",
    "महिला उद्यमी", "महिला उद्यमियों",
    "महिला लाभार्थी",
    "महिलाओ", "महिलाओ के लिए",
    "महिलाओं के लिए",
    "महिलांना", "महिलांसाठी",
    "महिला उद्योजक", "महिला उद्योजिका",
    "महिला लाभार्थी",
]


# ============================================================
# QUERY NORMALIZATION
# ============================================================

def normalize_query(query):
    """
    Normalize a question while preserving Hindi, Marathi,
    English and other Unicode characters.
    """

    query = str(query).lower().strip()
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
    return " ".join(query.split()).strip()


# ============================================================
# DETECT GOVERNMENT SCHEMES
# ============================================================

def detect_scheme(query):

    normalized_query = normalize_query(query)
    detected_schemes = []

    for scheme, keywords in SCHEME_KEYWORDS.items():

        for keyword in keywords:
            keyword_normalized = normalize_query(keyword)

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
            keyword_normalized = normalize_query(keyword)

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
            keyword_normalized = normalize_query(keyword)

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
# WOMEN-SPECIFIC GOVERNMENT SCHEME SEARCHES
# ============================================================

WOMEN_SCHEME_QUERIES = [
    # English
    "government schemes for women entrepreneurs in India",
    "government financial assistance for rural women",
    "government loan schemes for women entrepreneurs",
    "women self help group government schemes",
    "women entrepreneurship government support",
    "government subsidies for women entrepreneurs",
    "women beneficiaries government schemes",
    "rural women livelihood government schemes",

    # Hindi
    "महिलाओं के लिए सरकारी योजनाएं",
    "महिला उद्यमियों के लिए सरकारी योजनाएं",
    "ग्रामीण महिलाओं के लिए सरकारी योजनाएं",
    "महिलाओं के लिए सरकारी लोन योजनाएं",
    "महिला स्वयं सहायता समूह सरकारी योजना",
    "महिला उद्यमियों के लिए वित्तीय सहायता",
    "महिलाओं के लिए रोजगार और स्वरोजगार योजनाएं",
    "महिला लाभार्थियों के लिए सरकारी सहायता",

    # Marathi
    "महिलांसाठी सरकारी योजना",
    "महिला उद्योजकांसाठी सरकारी योजना",
    "ग्रामीण महिलांसाठी सरकारी योजना",
    "महिलांसाठी कर्ज योजना",
    "महिला बचत गट सरकारी योजना",
    "महिला उद्योजकांसाठी आर्थिक मदत",
    "महिलांसाठी रोजगार योजना",
]


# ============================================================
# QUERY EXPANSION
# ============================================================

def expand_query(query):

    normalized_query = normalize_query(query)

    schemes = detect_scheme(query)
    categories = detect_categories(query)
    topics = detect_topics(query)
    women_related = is_women_related(query)

    expanded_queries = [query]

    # --------------------------------------------------------
    # MUDRA
    # --------------------------------------------------------

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
        ])

    # --------------------------------------------------------
    # PMEGP
    # --------------------------------------------------------

    if "pmegp" in schemes:

        expanded_queries.extend([
            "PMEGP eligibility",
            "PMEGP women entrepreneurs",
            "PMEGP special category women",
            "PMEGP subsidy rural women",
            "PMEGP beneficiary contribution women",
            "PMEGP loan amount and subsidy",
            "PMEGP project cost limits",
            "Prime Minister Employment Generation Programme benefits",
            "प्रधानमंत्री रोजगार सृजन कार्यक्रम पात्रता",
            "पीएमईजीपी योजना महिलाओं के लिए",
            "रोजगार सृजन योजना सब्सिडी",
            "PMEGP महिला उद्योजक अनुदान",
        ])

    # --------------------------------------------------------
    # PM VISHWAKARMA
    # --------------------------------------------------------

    if "pm_vishwakarma" in schemes:

        expanded_queries.extend([
            "PM Vishwakarma eligibility",
            "PM Vishwakarma women artisans",
            "PM Vishwakarma benefits",
            "PM Vishwakarma loan",
            "PM Vishwakarma government scheme",
            "PM Vishwakarma training and toolkit incentive",
            "PM Vishwakarma loan interest rate",
            "PM Vishwakarma registration process",
            "प्रधानमंत्री विश्वकर्मा योजना पात्रता",
            "विश्वकर्मा योजना के लाभ",
            "विश्वकर्मा योजना के तहत ऋण",
            "विश्वकर्मा योजना प्रशिक्षण और टूलकिट",
            "विश्वकर्मा योजना महिला कारीगर",
        ])

    # --------------------------------------------------------
    # PMFME
    # --------------------------------------------------------

    if "pmfme" in schemes:

        expanded_queries.extend([
            "PMFME eligibility",
            "PMFME women entrepreneurs",
            "PMFME food processing benefits",
            "PMFME financial assistance",
            "PMFME micro food processing enterprises",
            "PMFME subsidy and credit linked support",
        ])

    # --------------------------------------------------------
    # DAY-NRLM
    # --------------------------------------------------------

    if "day_nrlm" in schemes:

        expanded_queries.extend([
            "DAY NRLM women",
            "DAY NRLM self help groups",
            "DAY NRLM women entrepreneurs",
            "DAY NRLM rural women livelihood",
            "DAY NRLM benefits",
            "DAY NRLM financial assistance SHG",
        ])

    # --------------------------------------------------------
    # CGTMSE
    # --------------------------------------------------------

    if "cgtmse" in schemes:

        expanded_queries.extend([
            "CGTMSE eligibility",
            "CGTMSE women entrepreneurs",
            "CGTMSE credit guarantee",
            "CGTMSE collateral free loan",
            "CGTMSE benefits",
        ])

    # --------------------------------------------------------
    # MAHARASHTRA GOVERNMENT SCHEMES
    # --------------------------------------------------------

    if "maharashtra_schemes" in schemes:

        expanded_queries.extend([
            "Maharashtra government schemes women entrepreneurs",
            "Maharashtra women entrepreneurship scheme",
            "Maharashtra government entrepreneurship benefits",
            "Maharashtra rural women financial assistance",
        ])

    # --------------------------------------------------------
    # WOMEN-SPECIFIC SEARCH EXPANSION
    # --------------------------------------------------------

    if women_related:

        expanded_queries.extend(WOMEN_SCHEME_QUERIES)

        # Search for the major schemes relevant to women.
        expanded_queries.extend([
            "MUDRA loan for women entrepreneurs",
            "PMEGP subsidy for women entrepreneurs",
            "PM Vishwakarma benefits for women artisans",
            "DAY NRLM women self help groups",
            "PMFME women food processing entrepreneurs",
            "CGTMSE loans for women entrepreneurs",
        ])

    # --------------------------------------------------------
    # GENERAL KNOWLEDGE EXPANSION
    # --------------------------------------------------------

    if not schemes:

        if "entrepreneurship" in categories:

            expanded_queries.extend([
                "how to start a small business",
                "entrepreneurship basics",
                "small business planning",
                "business planning for women entrepreneurs",
                "starting a rural business",
            ])

        if "digital_skills" in categories:

            expanded_queries.extend([
                "digital skills for women entrepreneurs",
                "smartphone basics",
                "internet basics",
                "digital payments",
                "online banking",
                "government online portals",
            ])

        if "digital_marketing" in categories:

            expanded_queries.extend([
                "digital marketing for small business",
                "WhatsApp Business for entrepreneurs",
                "social media marketing for small business",
                "online selling",
                "product promotion",
                "customer communication",
            ])

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

        if "business_compliance" in categories:

            expanded_queries.extend([
                "Udyam registration",
                "GST registration",
                "PAN for business",
                "business licences",
                "business registration requirements",
            ])

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

    # --------------------------------------------------------
    # REMOVE DUPLICATES
    # --------------------------------------------------------

    unique_queries = []
    seen = set()

    for search_query in expanded_queries:

        normalized_search = normalize_query(search_query)

        if normalized_search not in seen:

            seen.add(normalized_search)
            unique_queries.append(search_query)

    return {
        "original_query": query,
        "normalized_query": normalized_query,
        "detected_schemes": schemes,
        "detected_categories": categories,
        "detected_topics": topics,
        "women_related": women_related,
        "expanded_queries": unique_queries,
    }


# ============================================================
# MAIN QUERY ROUTER
# ============================================================

def route_query(query):

    return expand_query(query)


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
            print("-", scheme)

    else:
        print("- No specific scheme detected")

    print("\nDetected Categories:")

    if result["detected_categories"]:

        for category in result["detected_categories"]:
            print("-", category)

    else:
        print("- No specific category detected")

    print("\nDetected Topics:")

    if result["detected_topics"]:

        for topic in result["detected_topics"]:
            print("-", topic)

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

    print("\nTotal Expanded Queries:")
    print(len(result["expanded_queries"]))
