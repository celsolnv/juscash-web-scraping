import re

def extract_info(text: str):
    results = []

    # Split the text by publications using "Processo nnnnn..." pattern
    entries = re.split(r"(?:\n|^)(Processo\s+\d{7}-\d{2}\.\d{4}\.\d{1}\.\d{2}\.\d{4})", text)

    # Reassemble the split results in pairs: [label, content]
    for i in range(1, len(entries), 2):
        case_number = entries[i]
        content = entries[i + 1]
        full_block = f"{case_number}{content}"

        # Extract plaintiff
        plaintiff_match = re.search(r"[-–]\s*(.*?)\s*-\s*Vistos", full_block)
        plaintiff = plaintiff_match.group(1).strip() if plaintiff_match else None

        # Extract attorneys
        attorneys = re.findall(r"ADV: ([A-Z\s]+)\s*\(OAB.*?\)", full_block)
        attorney = "; ".join(attorneys) if attorneys else None

        # Extract values
        value_principal = re.search(r"R\$ ?([\d\.,]+)\s*-\s*principal", full_block, re.IGNORECASE)
        value_interest = re.search(r"R\$ ?([\d\.,]+)\s*-\s*juros", full_block, re.IGNORECASE)
        value_attorney = re.search(r"R\$ ?([\d\.,]+)\s*-\s*honorários", full_block, re.IGNORECASE)

        results.append({
            "case_number": case_number.replace("Processo", "").strip(),
            "plaintiff": plaintiff,
            "attorney": attorney,
            "value_principal": value_principal.group(1) if value_principal else None,
            "value_interest": value_interest.group(1) if value_interest else None,
            "value_attorney": value_attorney.group(1) if value_attorney else None,
            # "full_text": full_block,
            "defendant": "Instituto Nacional do Seguro Social - INSS",
            "status": "new"
        })

    # Select the most complete entry (based on filled fields)
    def count_filled_fields(entry):
        fields = ['case_number', 'plaintiff', 'attorney', 'value_principal', 'value_interest', 'value_attorney']
        return sum(1 for f in fields if entry.get(f))

    most_complete = max(results, key=count_filled_fields, default=None)
    return most_complete
