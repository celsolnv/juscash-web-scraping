import re

def extract_info(text: str, published_at: str):
    results = []

    # Split by each "Processo xxx" publication
    entries = re.split(r"(?:\n|^)(Processo\s+\d{7}-\d{2}\.\d{4}\.\d{1}\.\d{2}\.\d{4})", text)

    for i in range(1, len(entries), 2):
        case_number = entries[i]
        content = entries[i + 1]
        full_block = f"{case_number}{content}"

        # Extract plaintiff
        plaintiff_match = re.search(r"[-–]\s*(.*?)\s*-\s*Vistos", full_block)
        plaintiff = plaintiff_match.group(1).strip() if plaintiff_match else ""

        # Extract attorneys
        attorneys = re.findall(r"ADV: ([A-Z\s]+)\s*\(OAB.*?\)", full_block)
        attorney = "; ".join(attorneys).strip() if attorneys else ""

        # Extract and format monetary values with comma
        def extract_val(label):
            match = re.search(rf"R\$ ?([\d\.,]+)\s*-\s*{label}", full_block, re.IGNORECASE)
            if not match:
                return ""
            raw = match.group(1).replace(".", "").replace(",", ".")
            return raw

        value_principal = extract_val("principal")
        value_interest = extract_val("juros")
        value_attorney = extract_val("honorários")

        results.append({
            "case_number": case_number.replace("Processo", "").strip(),
            "plaintiff": plaintiff,
            "attorney": attorney,
            "value_principal": value_principal,
            "value_interest": value_interest,
            "value_attorney": value_attorney,
            "published_at": published_at,
            "full_text": full_block.strip(),
            "defendant": "Instituto Nacional do Seguro Social - INSS",
            "status": "new"
        })

    # Select the most complete entry (based on filled fields)
    def count_filled_fields(entry):
        fields = ['case_number', 'plaintiff', 'attorney', 'value_principal', 'value_interest', 'value_attorney']
        return sum(1 for f in fields if entry.get(f))

    most_complete = max(results, key=count_filled_fields, default=None)

    if most_complete:
        most_complete = {k: v for k, v in most_complete.items() if v}

    return most_complete
