from datetime import datetime
from typing import List, Optional, Tuple
import streamlit as st
import re

def generate_common_4():
    pins = set()
    for i in range(10):
        pins.add(str(i) * 4)
    for i in range(7):
        pins.add(f"{i}{i+1}{i+2}{i+3}")
    for i in range(9, 2, -1):
        pins.add(f"{i}{i-1}{i-2}{i-3}")
    extra = ['1212', '1122', '1010', '2020', '6969']
    pins.update(extra)
    return pins

def generate_common_6():
    pins = set()
    for i in range(10):
        pins.add(str(i) * 6)
    for i in range(5):
        seq = ''.join(str((i + j) % 10) for j in range(6))
        pins.add(seq)
    for i in range(9, 4, -1):
        seq = ''.join(str((i - j) % 10) for j in range(6))
        pins.add(seq)
    extra = ['123456', '654321', '112233', '102030']
    pins.update(extra)
    return pins

def is_common_mpin(pin):
    if len(pin) not in [4, 6] or not pin.isdigit():
        return 'INVALID', ['INVALID_FORMAT']
    reasons = []
    if len(pin) == 4 and pin in generate_common_4():
        reasons.append('COMMONLY_USED')
    if len(pin) == 6 and pin in generate_common_6():
        reasons.append('COMMONLY_USED')
    return ('WEAK' if reasons else 'STRONG'), reasons

def date_patterns(date_str):
    if not date_str:
        return []
    try:
        y, m, d = date_str.split('-')
        sy = y[-2:]
        return [d + m, m + d, d + sy, sy + d, m + sy, sy + m, y,
                d + m + sy, m + d + sy, sy + m + d, d + m + y, m + d + y]
    except:
        return []


def evaluate_mpin(mpin: str, dob: Optional[str] = None, spouse_dob: Optional[str] = None, anniversary: Optional[str] = None) -> Tuple[str, List[str]]:
    """Evaluate MPIN strength using regex-enhanced pattern matching"""
    
    # Basic validation using regex
    if not mpin or not re.match(r'^\d{4}$|^\d{6}$', mpin):
        return 'INVALID', ['INVALID_FORMAT']
    
    reasons = []
    
    # Check if commonly used
    common_strength, common_reasons = is_common_mpin(mpin)
    if common_strength == 'WEAK':
        reasons.extend(common_reasons)
    
    # Check demographic patterns
    demo_checks = [
        (dob, 'DEMOGRAPHIC_DOB_SELF'), 
        (spouse_dob, 'DEMOGRAPHIC_DOB_SPOUSE'), 
        (anniversary, 'DEMOGRAPHIC_ANNIVERSARY')
    ]

    for date_str, reason in demo_checks:
        if date_str:
            patterns = date_patterns(date_str)
            if mpin in patterns:
                reasons.append(reason)
    
    # Determine strength
    strength = 'WEAK' if reasons else 'STRONG'
    return strength, reasons

def display_result(strength: str, reasons: List[str]):
    """Display the MPIN evaluation result"""
    st.markdown("---")
    st.subheader("🔍 MPIN Evaluation Result")
    
    reason_descriptions = {
        'COMMONLY_USED': 'This MPIN is commonly used and easily guessable.',
        'DEMOGRAPHIC_DOB_SELF': 'This MPIN matches patterns from your date of birth.',
        'DEMOGRAPHIC_DOB_SPOUSE': 'This MPIN matches patterns from your spouse\'s date of birth.',
        'DEMOGRAPHIC_ANNIVERSARY': 'This MPIN matches patterns from your anniversary date.',
        'INVALID_FORMAT': 'Invalid format - MPIN must be 4 or 6 digits only.'
    }
    
    if strength == 'INVALID':
        st.error("❌ Invalid MPIN Format")
        for reason in reasons:
            st.write(f"{reason_descriptions.get(reason, reason)}")
    elif strength == 'STRONG':
        st.success("✅ STRONG - Your MPIN appears secure!")
        st.balloons()
    else:  
        st.warning("WEAK - Your MPIN could be easily guessed")
        st.write("*Reasons:*")
        for reason in reasons:
            st.write(f"{reason_descriptions.get(reason, reason)}")

def run_test_cases(user_mpin=None):
    """Run comprehensive test cases"""
    # Check if user entered invalid MPIN using regex
    force_all_fail = not user_mpin or not re.match(r'^\d{4}$|^\d{6}$', user_mpin)
    
    test_cases = [
        # Part A: Common MPINs (4-digit)
        ('1234', None, None, None, 'WEAK', ['COMMONLY_USED']),
        ('0000', None, None, None, 'WEAK', ['COMMONLY_USED']),
        ('1122', None, None, None, 'WEAK', ['COMMONLY_USED']),
        ('4567', None, None, None, 'WEAK', ['COMMONLY_USED']),
        ('8421', None, None, None, 'STRONG', []),
        
        # Part B & C: Demographics (4-digit)
        ('0201', '1998-01-02', None, None, 'WEAK', ['DEMOGRAPHIC_DOB_SELF']),
        ('0102', '1998-01-02', None, None, 'WEAK', ['DEMOGRAPHIC_DOB_SELF']),
        ('0298', '1998-01-02', None, None, 'WEAK', ['DEMOGRAPHIC_DOB_SELF']),
        ('9802', '1998-01-02', None, None, 'WEAK', ['DEMOGRAPHIC_DOB_SELF']),
        ('1585', None, '1985-02-15', None, 'WEAK', ['DEMOGRAPHIC_DOB_SPOUSE']),
        ('0215', None, '1985-02-15', None, 'WEAK', ['DEMOGRAPHIC_DOB_SPOUSE']),
        ('1406', None, None, '2020-06-14', 'WEAK', ['DEMOGRAPHIC_ANNIVERSARY']),
        ('2025', None, None, '2025-06-14', 'WEAK', ['DEMOGRAPHIC_ANNIVERSARY']),
        
        # Part D: 6-digit MPINs
        ('123456', None, None, None, 'WEAK', ['COMMONLY_USED']),
        ('000000', None, None, None, 'WEAK', ['COMMONLY_USED']),
        ('654321', None, None, None, 'WEAK', ['COMMONLY_USED']),
        ('020198', '1998-01-02', None, None, 'WEAK', ['DEMOGRAPHIC_DOB_SELF']),
        ('010298', '1998-01-02', None, None, 'WEAK', ['DEMOGRAPHIC_DOB_SELF']),
        ('980201', '1998-01-02', None, None, 'WEAK', ['DEMOGRAPHIC_DOB_SELF']),
        ('140620', None, None, '2020-06-14', 'WEAK', ['DEMOGRAPHIC_ANNIVERSARY']),
        ('789135', None, None, None, 'STRONG', []),
    ]
    
    st.markdown("---")
    st.subheader("Test Cases Results")
    
    if force_all_fail:
        st.warning(f"Invalid MPIN format detected: '{user_mpin}' - All test cases will FAIL!")
        st.info("Only 4-digit and 6-digit numeric MPINs are valid.")
    
    passed = 0
    total = len(test_cases)
    
    for i, (mpin, dob, spouse_dob, anniversary, expected_strength, expected_reasons) in enumerate(test_cases, 1):
        actual_strength, actual_reasons = evaluate_mpin(mpin, dob, spouse_dob, anniversary)
        
        # If user entered invalid MPIN, force all tests to fail
        if force_all_fail:
            st.error(f"Test {i}: ❌ FAILED")
            st.write(f"*MPIN:* {mpin}")
            st.write(f"*Expected:* {expected_strength}, {expected_reasons}")
            st.write(f"*Actual:* {actual_strength}, {actual_reasons}")
            st.write("Invalid MPIN format")
        else:
            # Normal test logic
            expected_reasons_sorted = sorted(expected_reasons)
            actual_reasons_sorted = sorted(actual_reasons)
            
            if actual_strength == expected_strength and actual_reasons_sorted == expected_reasons_sorted:
                st.success(f"Test {i}: ✅ PASSED")
                passed += 1
            else:
                st.error(f"Test {i}: ❌ FAILED")
                st.write(f"*MPIN:* {mpin}")
                st.write(f"*Expected:* {expected_strength}, {expected_reasons}")
                st.write(f"*Actual:* {actual_strength}, {actual_reasons}")
    
    if force_all_fail:
        st.error(f"0/{total} test cases passed (All failed due to invalid MPIN format)")
    else:
        st.info(f"*Results: {passed}/{total} test cases passed*")
        if passed == total:
            st.success("🎉 All test cases passed!")
            st.balloons()

def main():
    st.set_page_config(page_title="MPIN Strength Checker", layout="centered")
    st.title("🔐 MPIN Strength Checker")
    st.write("Check if your MPIN is secure based on common patterns and personal demographics.")

    # MPIN input with regex validation
    mpin = st.text_input("Enter your MPIN (4 or 6 digits)", max_chars=6, type="password")
    
    # Show validation feedback
    if mpin and not re.match(r'^\d{4}$|^\d{6}$', mpin):
        st.error("MPIN must be exactly 4 or 6 digits")

    # Date inputs (optional)
    min_date = datetime(1900, 1, 1)
    max_date = datetime.now().date()
    dob = None
    spouse_dob = None
    anniversary = None
    
    with st.expander("Optional: Include Personal Dates for Enhanced Security Check"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.checkbox("Your Date of Birth?"):
                dob = st.date_input("Your Date of Birth", key="dob", min_value=min_date, max_value=max_date)
        
        with col2:
            if st.checkbox("Spouse's Date of Birth?"):
                spouse_dob = st.date_input("Spouse's Date of Birth", key="spouse_dob", min_value=min_date, max_value=max_date)
        
        with col3:
            if st.checkbox("Anniversary Date?"):
                anniversary = st.date_input("Anniversary Date", key="anniv", min_value=min_date, max_value=max_date)

    # Convert dates to strings
    dob_str = dob.strftime('%Y-%m-%d') if dob else None
    spouse_dob_str = spouse_dob.strftime('%Y-%m-%d') if spouse_dob else None
    anniversary_str = anniversary.strftime('%Y-%m-%d') if anniversary else None

    # Button row
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Evaluate MPIN
        if st.button("Check MPIN Strength", type="primary"):
            if mpin:
                strength, reasons = evaluate_mpin(mpin, dob_str, spouse_dob_str, anniversary_str)
                display_result(strength, reasons)
            else:
                st.warning("Please enter an MPIN to check.")
    
    with col2:
        # Run test cases
        if st.button("Run Test Cases"):
            run_test_cases(mpin)

if __name__ == "__main__":
    main()