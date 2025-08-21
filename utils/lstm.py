import torch
import torch.nn as nn
import os

class LSTMModel(nn.Module):
    def __init__(self, input_size: int, hidden_size: int = 64, output_size: int = 1):
        super().__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        out, _ = self.lstm(x)
        return self.fc(out[:, -1, :])

def encode_blood_group(bg: str) -> int:
    mapping = {'O-':0,'O+':1,'A-':2,'A+':3,'B-':4,'B+':5,'AB-':6,'AB+':7}
    return mapping.get(bg, -1)

def encode_organ(organ: str) -> int:
    valid_organs = {'kidney': 0, 'heart': 1, 'liver': 2, 'lung': 3}
    if organ is None:
        return -1
    organ_lower = organ.lower()
    return valid_organs.get(organ_lower, -1)

def encode_hla(val) -> int:
    # New: HLA values are numeric, so convert directly to int
    try:
        return int(val)
    except Exception:
        return -1

def is_blood_compatible(r_bg: str, d_bg: str) -> bool:
    table = {
        'O-': ['O-'],
        'O+': ['O-', 'O+'],
        'A-': ['O-', 'A-'],
        'A+': ['O-', 'O+', 'A-', 'A+'],
        'B-': ['O-', 'B-'],
        'B+': ['O-', 'O+', 'B-', 'B+'],
        'AB-': ['O-', 'A-', 'B-', 'AB-'],
        'AB+': ['O-', 'O+', 'A-', 'A+', 'B-', 'B+', 'AB-', 'AB+']
    }
    return d_bg in table.get(r_bg, [])

def load_lstm_model():
    model_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'lstm_model.pth')
    model = LSTMModel(input_size=9)
    if not os.path.exists(model_path):
        print("Model file not found, returning untrained model.")
        return model
    if os.path.getsize(model_path) < 100:
        raise EOFError("Model file appears to be empty or corrupted.")
    model.load_state_dict(torch.load(model_path))
    model.eval()
    return model

import difflib

def encode_organ(organ: str) -> int:
    valid_organs = {'kidney': 0, 'heart': 1, 'liver': 2, 'lung': 3}
    if organ is None:
        return -1
    organ_lower = organ.lower()
    if organ_lower in valid_organs:
        return valid_organs[organ_lower]
    # Try to find close match
    close_matches = difflib.get_close_matches(organ_lower, valid_organs.keys(), n=1, cutoff=0.7)
    if close_matches:
        print(f"Warning: '{organ}' not recognized, using close match '{close_matches[0]}'")
        return valid_organs[close_matches[0]]
    print(f"Unknown organ: {organ}")
    return -1



#def predict_match(receiver, donor, model: LSTMModel) -> bool:
    #rbg = receiver.blood_group
    #dbg = donor.blood_group

    #print(f"Testing match for Receiver {receiver.name} with Donor {donor.hla_a}")
    #print(f"Receiver organ_needed: {receiver.organ_needed}")

    #if not is_blood_compatible(rbg, dbg):
        #print("Incompatible blood group:", rbg, dbg)
        #return False

    #rf = [
        #encode_blood_group(rbg),
        #encode_organ(receiver.organ_needed),  # This prints debug
        #encode_hla(receiver.hla_a),
        #encode_hla(receiver.hla_b),
        #encode_hla(receiver.hla_dr)
    #]
    #df = [
        #encode_blood_group(dbg),
        #encode_hla(donor.hla_a),
        #encode_hla(donor.hla_b),
        #encode_hla(donor.hla_dr)
    #]

    #print("Receiver features:", rf)
    #print("Donor features:", df)

    #if -1 in rf + df:
        #print("Invalid encoding. Check HLA or other values.")
        #return False

    #feats = torch.tensor([[rf + df]], dtype=torch.float32)
    #with torch.no_grad():
        #score = model(feats).item()
        #print("LSTM score:", score)

    #return score > -5
def parse_hla(hla_str):
    if not hla_str:
        return set()
    return set(int(val.strip()) for val in hla_str.split(',') if val.strip().isdigit())

# def predict_match(receiver, donor, model: LSTMModel) -> tuple[bool, float]:
#     rbg = receiver.blood_group
#     dbg = donor.blood_group

#     print(f"Testing match for Receiver {receiver.name} with Donor {donor.full_name}")
#     print(f"Receiver organ_needed: {receiver.organ_needed}")

#     if not is_blood_compatible(rbg, dbg):
#         print("Incompatible blood group:", rbg, dbg)
#         return False, 0.0  # Return score 0.0 on failure

#     # Encode
#     receiver_blood = encode_blood_group(rbg)
#     donor_blood = encode_blood_group(dbg)
#     organ = encode_organ(receiver.organ_needed)

#     r_hla_a = parse_hla(receiver.hla_a)
#     r_hla_b = parse_hla(receiver.hla_b)
#     r_hla_dr = parse_hla(receiver.hla_dr)
#     d_hla_a = parse_hla(donor.hla_a)
#     d_hla_b = parse_hla(donor.hla_b)
#     d_hla_dr = parse_hla(donor.hla_dr)

#     match_a = 1 if r_hla_a & d_hla_a else 0
#     match_b = 1 if r_hla_b & d_hla_b else 0
#     match_dr = 1 if r_hla_dr & d_hla_dr else 0

#     features = [
#         receiver_blood,
#         organ,
#         match_a,
#         match_b,
#         match_dr,
#         donor_blood,
#         match_a,
#         match_b,
#         match_dr
#     ]

#     print("Input features:", features)

#     if -1 in features:
#         print("Invalid encoding in features.")
#         return False, 0.0

#     feats = torch.tensor([[features]], dtype=torch.float32)

#     with torch.no_grad():
#         score = model(feats).item()
#         print("LSTM score:", score)

#     is_match = score > -5  # use a better threshold later
#     return is_match, score

def predict_match(receiver, donor, model: LSTMModel) -> tuple[bool, float]:
    rbg = receiver.blood_group
    dbg = donor.blood_group

    print(f"Testing match for Receiver {receiver.name} with Donor {donor.full_name}")
    print(f"Receiver organ_needed: {receiver.organ_needed}, Donor organ: {donor.organ}")

    # Check blood group compatibility
    if not is_blood_compatible(rbg, dbg):
        print("Incompatible blood group:", rbg, dbg)
        return False, 0.0

    # Check organ match
    if receiver.organ_needed.strip().lower() != donor.organ.strip().lower():
        print("Incompatible organ type:", receiver.organ_needed, donor.organ)
        return False, 0.0

    # Encode features
    receiver_blood = encode_blood_group(rbg)
    donor_blood = encode_blood_group(dbg)
    organ = encode_organ(receiver.organ_needed)

    r_hla_a = parse_hla(receiver.hla_a)
    r_hla_b = parse_hla(receiver.hla_b)
    r_hla_dr = parse_hla(receiver.hla_dr)
    d_hla_a = parse_hla(donor.hla_a)
    d_hla_b = parse_hla(donor.hla_b)
    d_hla_dr = parse_hla(donor.hla_dr)

    match_a = 1 if r_hla_a & d_hla_a else 0
    match_b = 1 if r_hla_b & d_hla_b else 0
    match_dr = 1 if r_hla_dr & d_hla_dr else 0

    features = [
        receiver_blood,
        organ,
        match_a,
        match_b,
        match_dr,
        donor_blood,
        match_a,
        match_b,
        match_dr
    ]

    print("Input features:", features)

    if -1 in features:
        print("Invalid encoding in features.")
        return False, 0.0

    feats = torch.tensor([[features]], dtype=torch.float32)

    with torch.no_grad():
        score = model(feats).item()
        print("LSTM score:", score)

    is_match = score > -5  # adjustable threshold
    return is_match, score



