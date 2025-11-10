#!/usr/bin/env python3
"""
SOaC Framework - Detection Rules Importer
Imports detection rules from Excel files into the framework
"""

import pandas as pd
import requests
import json
import sys
import os

# API Configuration
API_BASE_URL = "http://localhost:5001/api"

def clean_cql_query(rows):
    """Combine multi-row CQL queries into a single query"""
    cql_lines = []
    for row in rows:
        if pd.notna(row) and str(row).strip():
            cql_lines.append(str(row).strip())
    return " | ".join(cql_lines) if cql_lines else ""

def import_entraid_rules():
    """Import EntraID authentication rules"""
    print("📥 Importing EntraID Authentication Rules...")
    
    try:
        df = pd.read_excel('EntraID_Authentication_Rules.xlsx')
        
        rules_imported = 0
        current_rule = None
        cql_buffer = []
        
        for idx, row in df.iterrows():
            # Check if this is a new rule (has a rule number)
            if pd.notna(row.get('#')):
                # Save previous rule if exists
                if current_rule and cql_buffer:
                    current_rule['cql_query'] = clean_cql_query(cql_buffer)
                    response = requests.post(f"{API_BASE_URL}/detection-rules", json=current_rule)
                    if response.status_code == 201:
                        rules_imported += 1
                        print(f"  ✓ Imported: {current_rule['name']}")
                    else:
                        print(f"  ✗ Failed: {current_rule['name']} - {response.text}")
                
                # Start new rule
                current_rule = {
                    'name': str(row.get('Detection Rule', 'Unnamed Rule')),
                    'platform': 'entraid',
                    'severity': str(row.get('Severity', 'medium')).lower(),
                    'use_case': str(row.get('Use Case', 'intrusion')).lower(),
                    'mitre_tactic': str(row.get('MITRE Tactic', '')),
                    'mitre_technique': str(row.get('MITRE Technique', '')),
                    'category': str(row.get('Category', '')),
                    'incident_rule': str(row.get('Incident Rule', '')),
                    'enabled': True
                }
                cql_buffer = []
            
            # Collect CQL query lines
            if pd.notna(row.get('CQL Detection Query Template')):
                cql_buffer.append(row.get('CQL Detection Query Template'))
        
        # Don't forget the last rule
        if current_rule and cql_buffer:
            current_rule['cql_query'] = clean_cql_query(cql_buffer)
            response = requests.post(f"{API_BASE_URL}/detection-rules", json=current_rule)
            if response.status_code == 201:
                rules_imported += 1
                print(f"  ✓ Imported: {current_rule['name']}")
        
        print(f"✅ EntraID: Imported {rules_imported} rules\n")
        return rules_imported
        
    except Exception as e:
        print(f"❌ Error importing EntraID rules: {e}")
        return 0

def import_paloalto_rules():
    """Import Palo Alto NGFW rules"""
    print("📥 Importing Palo Alto NGFW Rules...")
    
    try:
        df = pd.read_excel('PaloAlto_NGFW_Rules.xlsx')
        
        rules_imported = 0
        current_rule = None
        cql_buffer = []
        
        for idx, row in df.iterrows():
            # Check if this is a new rule (has a rule number)
            if pd.notna(row.get('#')):
                # Save previous rule if exists
                if current_rule and cql_buffer:
                    current_rule['cql_query'] = clean_cql_query(cql_buffer)
                    response = requests.post(f"{API_BASE_URL}/detection-rules", json=current_rule)
                    if response.status_code == 201:
                        rules_imported += 1
                        print(f"  ✓ Imported: {current_rule['name']}")
                    else:
                        print(f"  ✗ Failed: {current_rule['name']} - {response.text}")
                
                # Start new rule
                current_rule = {
                    'name': str(row.get('Detection Rule', 'Unnamed Rule')),
                    'platform': 'paloalto',
                    'severity': str(row.get('Severity', 'medium')).lower(),
                    'use_case': str(row.get('Use Case', 'intrusion')).lower(),
                    'mitre_tactic': str(row.get('MITRE Tactic', '')),
                    'mitre_technique': str(row.get('MITRE Technique', '')),
                    'category': str(row.get('Category', '')),
                    'incident_rule': str(row.get('Incident Rule', '')),
                    'enabled': True
                }
                cql_buffer = []
            
            # Collect CQL query lines
            if pd.notna(row.get('CQL Detection Query Template')):
                cql_buffer.append(row.get('CQL Detection Query Template'))
        
        # Don't forget the last rule
        if current_rule and cql_buffer:
            current_rule['cql_query'] = clean_cql_query(cql_buffer)
            response = requests.post(f"{API_BASE_URL}/detection-rules", json=current_rule)
            if response.status_code == 201:
                rules_imported += 1
                print(f"  ✓ Imported: {current_rule['name']}")
        
        print(f"✅ Palo Alto: Imported {rules_imported} rules\n")
        return rules_imported
        
    except Exception as e:
        print(f"❌ Error importing Palo Alto rules: {e}")
        return 0

def main():
    """Main import function"""
    print("=" * 60)
    print("SOaC Framework - Detection Rules Importer")
    print("=" * 60)
    print()
    
    # Check if API is accessible
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        if response.status_code != 200:
            print("❌ API is not accessible. Make sure Docker containers are running.")
            sys.exit(1)
        print("✓ API is healthy\n")
    except Exception as e:
        print(f"❌ Cannot connect to API: {e}")
        print("   Make sure to run: docker-compose up -d")
        sys.exit(1)
    
    # Import rules
    total_imported = 0
    total_imported += import_entraid_rules()
    total_imported += import_paloalto_rules()
    
    print("=" * 60)
    print(f"🎉 Import Complete! Total rules imported: {total_imported}")
    print("=" * 60)
    print()
    print("📊 View your rules:")
    print(f"   curl {API_BASE_URL}/detection-rules")
    print()
    print("📈 Check stats:")
    print(f"   curl {API_BASE_URL}/stats")
    print()

if __name__ == "__main__":
    main()