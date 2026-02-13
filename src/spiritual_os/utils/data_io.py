"""
Data Import/Export Utilities

Enable parishes to:
- Import existing member lists from spreadsheets
- Export data for backups
- Migrate from other parish software
- Maintain data ownership

Supported formats:
- CSV (universal)
- JSON (structured backup)
- Excel (common parish format)

Data portability is a core principle: parishes own their data.
"""

import csv
import json
from io import StringIO
from typing import List, Dict, Any, Optional
from datetime import datetime
from dataclasses import dataclass, asdict


@dataclass
class MemberImport:
    """Parish member data for import"""
    first_name: str
    last_name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    zip_code: Optional[str] = None
    family_id: Optional[str] = None
    date_of_birth: Optional[str] = None
    baptism_date: Optional[str] = None
    confirmation_date: Optional[str] = None
    ministry: Optional[str] = None
    scc_name: Optional[str] = None
    notes: Optional[str] = None


@dataclass
class ExportManifest:
    """Metadata for data export"""
    export_date: str
    parish_name: str
    parish_id: str
    record_count: int
    data_types: List[str]  # ["members", "sccs", "catechists", "giving"]
    version: str = "1.0"


class DataImporter:
    """
    Import parish data from various formats
    """
    
    @staticmethod
    def parse_csv_members(csv_content: str) -> List[MemberImport]:
        """
        Parse CSV member list
        
        Expected columns (flexible order):
        - first_name, last_name (required)
        - email, phone, address, city, zip_code (optional)
        - family_id, date_of_birth (optional)
        - baptism_date, confirmation_date (optional)
        - ministry, scc_name, notes (optional)
        """
        members = []
        reader = csv.DictReader(StringIO(csv_content))
        
        # Normalize column names (handle variations)
        column_map = {
            'first name': 'first_name',
            'firstname': 'first_name',
            'last name': 'last_name',
            'lastname': 'last_name',
            'surname': 'last_name',
            'e-mail': 'email',
            'phone number': 'phone',
            'telephone': 'phone',
            'postal code': 'zip_code',
            'postcode': 'zip_code',
            'scc': 'scc_name',
            'small christian community': 'scc_name',
        }
        
        for row in reader:
            # Normalize keys
            normalized_row = {}
            for key, value in row.items():
                normalized_key = column_map.get(key.lower().strip(), key.lower().replace(' ', '_'))
                normalized_row[normalized_key] = value.strip() if value else None
            
            # Extract member data
            try:
                member = MemberImport(
                    first_name=normalized_row.get('first_name', ''),
                    last_name=normalized_row.get('last_name', ''),
                    email=normalized_row.get('email'),
                    phone=normalized_row.get('phone'),
                    address=normalized_row.get('address'),
                    city=normalized_row.get('city'),
                    zip_code=normalized_row.get('zip_code'),
                    family_id=normalized_row.get('family_id'),
                    date_of_birth=normalized_row.get('date_of_birth'),
                    baptism_date=normalized_row.get('baptism_date'),
                    confirmation_date=normalized_row.get('confirmation_date'),
                    ministry=normalized_row.get('ministry'),
                    scc_name=normalized_row.get('scc_name'),
                    notes=normalized_row.get('notes')
                )
                
                # Validate required fields
                if member.first_name and member.last_name:
                    members.append(member)
                    
            except Exception as e:
                print(f"Error parsing row: {e}")
                continue
        
        return members
    
    @staticmethod
    def validate_import(members: List[MemberImport]) -> Dict[str, Any]:
        """
        Validate imported data
        
        Returns validation report with:
        - total_records
        - valid_records
        - invalid_records
        - warnings (missing emails, duplicate names, etc.)
        """
        report = {
            'total_records': len(members),
            'valid_records': 0,
            'invalid_records': 0,
            'warnings': [],
            'errors': []
        }
        
        seen_names = set()
        
        for i, member in enumerate(members, 1):
            # Check required fields
            if not member.first_name or not member.last_name:
                report['errors'].append(f"Row {i}: Missing required field (first_name or last_name)")
                report['invalid_records'] += 1
                continue
            
            # Check for duplicates
            name_key = f"{member.first_name.lower()}_{member.last_name.lower()}"
            if name_key in seen_names:
                report['warnings'].append(f"Row {i}: Possible duplicate - {member.first_name} {member.last_name}")
            seen_names.add(name_key)
            
            # Check for missing recommended fields
            if not member.email and not member.phone:
                report['warnings'].append(f"Row {i}: No contact info (email or phone) for {member.first_name} {member.last_name}")
            
            # Validate email format (basic)
            if member.email and '@' not in member.email:
                report['warnings'].append(f"Row {i}: Invalid email format - {member.email}")
            
            report['valid_records'] += 1
        
        return report


class DataExporter:
    """
    Export parish data for backup or migration
    """
    
    @staticmethod
    def export_to_csv(data: List[Dict], filename: str = "export.csv") -> str:
        """
        Export data to CSV format
        
        Returns CSV string ready for download.
        """
        if not data:
            return ""
        
        # Get all unique keys from all records
        fieldnames = set()
        for record in data:
            fieldnames.update(record.keys())
        fieldnames = sorted(list(fieldnames))
        
        output = StringIO()
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
        
        return output.getvalue()
    
    @staticmethod
    def export_to_json(data: Dict[str, Any], metadata: ExportManifest) -> str:
        """
        Export complete parish data to JSON
        
        Includes metadata manifest for version control.
        """
        export_package = {
            'manifest': asdict(metadata),
            'data': data,
            'export_timestamp': datetime.utcnow().isoformat()
        }
        
        return json.dumps(export_package, indent=2, default=str)
    
    @staticmethod
    def create_backup(
        parish_id: str,
        parish_name: str,
        members: List[Dict],
        sccs: List[Dict],
        catechists: List[Dict],
        giving: List[Dict]
    ) -> str:
        """
        Create complete parish backup (JSON)
        """
        manifest = ExportManifest(
            export_date=datetime.now().strftime("%Y-%m-%d"),
            parish_name=parish_name,
            parish_id=parish_id,
            record_count=len(members) + len(sccs) + len(catechists) + len(giving),
            data_types=["members", "sccs", "catechists", "giving"]
        )
        
        data = {
            'members': members,
            'sccs': sccs,
            'catechists': catechists,
            'giving': giving
        }
        
        return DataExporter.export_to_json(data, manifest)


# ============================================================================
# TEMPLATE GENERATORS
# ============================================================================

class TemplateGenerator:
    """
    Generate CSV templates for data entry
    """
    
    @staticmethod
    def member_template() -> str:
        """Generate blank member import template"""
        headers = [
            'first_name', 'last_name', 'email', 'phone',
            'address', 'city', 'zip_code', 'family_id',
            'date_of_birth', 'baptism_date', 'confirmation_date',
            'ministry', 'scc_name', 'notes'
        ]
        
        # Create sample row
        sample_row = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'phone': '+254-722-123456',
            'address': '123 Main St',
            'city': 'Nairobi',
            'zip_code': '00100',
            'family_id': 'FAM001',
            'date_of_birth': '1980-01-15',
            'baptism_date': '1980-02-20',
            'confirmation_date': '1992-05-10',
            'ministry': 'Lector',
            'scc_name': 'St. Francis SCC',
            'notes': 'Active in youth ministry'
        }
        
        output = StringIO()
        writer = csv.DictWriter(output, fieldnames=headers)
        writer.writeheader()
        writer.writerow(sample_row)  # Include example
        
        return output.getvalue()
    
    @staticmethod
    def scc_template() -> str:
        """Generate blank SCC import template"""
        headers = [
            'name', 'location', 'meeting_day', 'meeting_time',
            'coordinator_name', 'coordinator_phone', 'family_count',
            'notes'
        ]
        
        sample_row = {
            'name': 'St. Francis SCC',
            'location': 'Westlands, near Sarit Centre',
            'meeting_day': 'Thursday',
            'meeting_time': '19:00',
            'coordinator_name': 'Mary Wanjiru',
            'coordinator_phone': '+254-722-123456',
            'family_count': '15',
            'notes': 'Very active community'
        }
        
        output = StringIO()
        writer = csv.DictWriter(output, fieldnames=headers)
        writer.writeheader()
        writer.writerow(sample_row)
        
        return output.getvalue()


# Usage examples
if __name__ == "__main__":
    # Example: Generate member template
    template = TemplateGenerator.member_template()
    print("Member Import Template:")
    print(template)
    
    # Example: Parse CSV
    sample_csv = """first_name,last_name,email,phone
John,Doe,john@example.com,+254-722-123456
Jane,Smith,jane@example.com,+254-733-234567"""
    
    members = DataImporter.parse_csv_members(sample_csv)
    print(f"\nParsed {len(members)} members")
    
    # Example: Validate
    report = DataImporter.validate_import(members)
    print(f"\nValidation: {report['valid_records']} valid, {report['invalid_records']} invalid")
