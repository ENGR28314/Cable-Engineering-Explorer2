# Cable Engineering Explorer

Interactive Streamlit catalog for security/alarm, fire/life safety, CCTV, CATV/coaxial, RF, audio/video, control, power, Ethernet and fiber-optic cables.

**Prepared by Engr. Syed Hassan Iqbal Shah**

## Features
- Search/filter the 68-entry cable reference catalog by category, cable, application, manufacturer, standards or evidence fields.
- Interactive detail panels for characteristics, specifications, applications, advantages and limitations.
- Category illustration gallery plus support for a public image URL per product and image upload for a session. The built-in visuals are illustrative diagrams, not manufacturer product photographs.
- Side-by-side comparison of up to four cable records.
- Expanded CSV upload/export fields for exact manufacturer/model, certified temperature range, rating type, standard, certificate/DoP ID, certification body, datasheet URL, certificate URL, image URL, verification status and notes.
- Filter to records whose evidence status is marked verified.

## Critical certification note
The family-level temperature values are **indicative only, not certified ratings**. The project does not invent certified temperature ranges. A certified range must be tied to the exact manufacturer and part number, and the rating type must be clear (operating, installation, conductor maximum, storage or short-circuit). Confirm the current manufacturer datasheet and applicable certificate/Declaration of Performance (DoP), standard, scope and jurisdiction. The `Verification status` field starts as unverified for all generic catalog entries.

The listed Zion fire cable label includes `Cca-s1a,d0,a1` in the supplied description. A CPR reaction-to-fire class is not, by itself, proof of circuit integrity/fire resistance or proof that a temperature range is certified. Verify the exact DoP/certificate and model.

## Run locally
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Deploy on GitHub + Streamlit Community Cloud
1. Upload the project files/folder to a GitHub repository.
2. In Streamlit Community Cloud, connect the repository.
3. Select the repository branch and `app.py` as the main file.
4. Deploy.

## CSV fields
Required base columns: `Category`, `Cable / Product`, `Characteristics`, `Key specifications to verify`, `Indicative operating temperature`, `Typical applications`, `Pros`, `Cons`.

Optional evidence/image columns: `Manufacturer`, `Exact model / part number`, `Certified operating temperature range`, `Temperature rating type`, `Applicable standard`, `Certificate / DoP ID`, `Certification body`, `Datasheet URL`, `Certificate URL`, `Image URL`, `Verification status`, `Verification notes`.

Use a direct, publicly accessible image URL in `Image URL` to display an official product snapshot in the deployed app. The image uploader in the app is session-only; uploaded files are not automatically committed to GitHub. For permanent images, add them to the repository and use a repository-hosted URL or update the catalog.

## Engineering limitations
This is a comparison and learning tool, not a substitute for current manufacturer documentation, project calculations or qualified engineering review. Standards and temperature limits vary by product construction, voltage class, jacket, installation method and jurisdiction. Ambiguous labels remain flagged for verification.
