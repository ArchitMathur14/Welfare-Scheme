import streamlit as st
import json
import os
def load_data(filepath='schemes_db.json'):
    if not os.path.exists(filepath):
        st.error(f"Cannot find data file: {filepath}")
        return []
    with open(filepath, 'r') as file:
         return json.load(file)
def filter_schemes(schemes, age, occupation, income):
    matched = []
    # Convert occupation to lower case for comparison
    occ_lower = occupation.lower()
    
    for s in schemes:
        # Check matching criteria
        age_valid = s['age_range']['min'] <= age <= s['age_range']['max']
        income_valid = s['max_income_limit'] >= income
        
        target_occs = [o.lower() for o in s['target_occupation']]
        occ_valid = ('all' in target_occs) or (occ_lower in target_occs)
        
        if age_valid and income_valid and occ_valid:
            matched.append(s)
            
    return matched
def main():
    st.set_page_config(page_title="Welfare Matching Portal", layout="wide")
    st.title("Indian Government Welfare Matching Portal")
    
    schemes = load_data()
    
    # Sidebar
    st.sidebar.header("Applicant Profile")
    age = st.sidebar.number_input("Age", min_value=1, max_value=120, value=22, step=1)
    
    occupations = ["Student", "Farmer", "Small Business Owner", "Unemployed"]
    occupation = st.sidebar.selectbox("Occupation", options=occupations)
    
    # Adjust format for large numbers
    income = st.sidebar.number_input("Annual Income (INR)", min_value=0, max_value=20000000, value=0, step=10000)
    
    st.markdown("### Your Matched Welfare Schemes")
    
    # Check matching
    matches = filter_schemes(schemes, age, occupation, income)
    
    if not matches:
         st.warning("No schemes match your current profile. Please adjust your details or check back later.")
    else:
        st.success(f"Found {len(matches)} suitable scheme(s) for your profile!")
        
        # Render the matched schemes
        for m in matches:
             with st.expander(m['scheme_name']):
                 st.write(f"**Description:** {m['description']}")
                 
                 st.markdown("**Application Checklist:**")
                 for item in m['application_checklist']:
                     st.markdown(f"- {item}")
                     
                 st.markdown(f"[Go to Official Portal]({m['official_link']})")
if __name__ == "__main__":
    main()
