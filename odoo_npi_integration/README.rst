	This module integrates odoo with National Plan and Provider Enumeration System
        (NPPES) 'https://npiregistry.cms.hhs.gov'. This module fetches Doctor details from NPPES registry
        and fills in the partner form. NPI Details can be auto fetched while creating new doctor record
        in the system or old doctor can be refreshed with new information fetched from NPPES registry.
        For old records this module gives one level of verification for the information fetched from NPPES
        so, that information can be verified before writing into the doctor record as information in
        NPPES registry can be stale.
