import streamlit as st
import pandas as pd
from io import BytesIO
from pathlib import Path
import re

st.set_page_config(page_title="Cable Engineering Explorer", page_icon="🔌", layout="wide")

st.title("🔌 Cable Engineering Explorer")
st.caption("Characteristics • Specifications • Operating temperatures • Applications • Pros & Cons")
st.markdown("**Prepared by Engr. Syed Hassan Iqbal Shah**")
st.info(
    "Engineering reference only: cable construction, ratings and compliance vary by manufacturer, "
    "voltage class, conductor size, insulation, installation method and jurisdiction. Temperature "
    "ranges below are indicative family-level guidance—not certified ratings. Always verify the exact "
    "manufacturer datasheet, applicable standards and project specification before selection."
)

# Family-level reference ranges are intentionally indicative. Avoid implying that every product
# under a family has identical construction, performance or temperature limits.
CATALOG = [
("Security & Alarm","Burglar Alarm Cable","Copper multi-core; commonly solid/stranded conductors with PVC or LSZH jacket; shielded variants available","Low-voltage signal; conductor count and gauge depend on panel/device","Often about -20 to +70°C for common PVC types; verify datasheet","Intruder detectors, keypads, alarm panels","Low cost; easy termination; broad availability","Not for mains power; long runs can suffer voltage drop/noise; not automatically fire-rated"),
("Security & Alarm","Access Control Cable","Multi-core control cable; may combine power pairs and signal conductors; shielded options","Conductor size, pair count and shielding are system-specific","Often about -20 to +70°C for common PVC types; verify datasheet","Card readers, door contacts, electric-lock control circuits","Combines several circuits; convenient installation","Voltage drop matters for locks; cable pinout and shielding must match system; not universally outdoor-rated"),
("Fire & Life Safety","Fire Alarm Cable (Zion Cca S1a,d0,a1; 0051-CPR-3475)","Control/communication cable identified by supplied product description; fire reaction class stated as Cca-s1a,d0,a1","Confirm CPR Declaration of Performance, EN 50575 scope, circuit integrity/fire resistance, conductor size and approvals","Must use the specific datasheet; do not infer operating limit from CPR class","Fire detection and alarm circuits where the product's approvals and local code permit","Specified reaction-to-fire performance may aid building fire-safety design","CPR reaction-to-fire class is not the same as circuit-integrity rating; exact certificate/DoP and local approval required"),
("Video Surveillance","CCTV Surveillance Cable – Global coax with power","Coaxial video path plus separate power conductors in a shared jacket","Impedance and power conductor gauge depend on design","Common indoor PVC products often around -20 to +70°C; outdoor variants differ","Analog CCTV cameras needing video and DC power","One cable run for video and power; straightforward retrofit","Power drop over distance; coax bandwidth/connector limits; confirm outdoor/UV rating"),
("Video Surveillance","CCTV Surveillance Cable – LAN cable with power","Twisted-pair data cable bundled with power conductors or designed for a specific camera system","Category, impedance, PoE compatibility and power conductor size are product-specific","Typically installation-dependent; confirm cable and connector ratings","IP cameras, networked surveillance and compatible powered devices","Convenient single run; supports network architecture","Bundled power is not automatically PoE compliant; verify data category and power/thermal limits"),
("Video Surveillance","CCTV Surveillance Cable – Europe coax with power","Coaxial video cable combined with power conductors; regional construction may vary","Check impedance, shielding, attenuation and power conductor size","Verify datasheet; common PVC examples around -20 to +70°C","CCTV video and camera power","Simplifies routing; familiar coax terminations","Regional variants are not interchangeable without checking electrical properties"),
("Video Surveillance","CCTV Surveillance Cable – OEM coax with power","OEM-specific coax and power combination","No universal specification; use OEM part number and datasheet","OEM datasheet required","OEM surveillance installations","Can match a specific system design","Specifications and availability vary; avoid selecting by name alone"),
("Video Surveillance","CCTV Surveillance Cable – R (catalog label)","Product label is incomplete/ambiguous; construction cannot be safely inferred","Identify full product name, impedance, conductor and shield before procurement","Unknown until exact product is identified","Only after product identity and system requirement are confirmed","May map to a vendor-specific product","Insufficient information for safe technical selection"),
("Video Surveillance","RG59 CCTV Coaxial Cable","75-ohm coax, commonly solid copper or copper-clad conductor with dielectric and braid/foil shield","Nominal 75 Ω; attenuation depends on conductor, dielectric and frequency","Often around -20 to +70°C for standard PVC versions; other jackets differ","Analog CCTV, composite video, short RF/video distribution runs","Flexible; widely available; easy to terminate","Higher attenuation than larger coax at many frequencies; quality varies by conductor/shield"),
("Video Surveillance","RG11 CCTV Coaxial Cable","Larger 75-ohm coax with lower attenuation than RG59 in many designs","Nominal 75 Ω; larger diameter and bend radius","Product-specific; check jacket and installation limits","Longer CCTV/video runs and distribution","Lower loss than RG59 in many comparable designs","Bulkier, less flexible, more difficult to route and terminate"),
("Video Surveillance","PK75 CCTV Coaxial Cable","75-ohm coax family/market designation; construction varies by supplier","Confirm exact impedance, attenuation and construction","Manufacturer datasheet required","CCTV/video systems designed for matching PK75 cable","May fit established regional systems","Designation alone does not guarantee equivalent performance"),
("CATV & Satellite","RG6 Coaxial Cable","75-ohm coax with dielectric, foil/braid shielding and outer jacket","Nominal 75 Ω; shielding and sweep range vary","Common PVC products often around -20 to +70°C; outdoor versions differ","CATV, satellite feeds, broadband and video distribution","Good general-purpose balance of size and loss","Connector quality and shielding matter; not all RG6 is suitable for direct burial"),
("CATV & Satellite","RG59 Coaxial Cable","Smaller 75-ohm coax","Nominal 75 Ω; generally more loss than RG6 at higher frequencies","Product-specific; often -20 to +70°C for PVC variants","Legacy CCTV, baseband video, short distribution runs","Compact and flexible","May be unsuitable for long broadband/satellite runs due to attenuation"),
("CATV & Satellite","RG11 Coaxial Cable","Large 75-ohm coax for lower-loss distribution","Nominal 75 Ω; check frequency attenuation and return loss","Manufacturer datasheet required","Long CATV runs, backbone/drop distribution","Lower attenuation than RG6 in many comparable designs","Large bend radius; heavier; more expensive termination"),
("CATV & Satellite","SAT Coaxial Cable","75-ohm coax designed for satellite IF/RF distribution; shielding is important","Check screening class, attenuation, DC pass and frequency range","Outdoor and UV ratings vary","Satellite dish to receiver/multiswitch","Purpose-built options for satellite use","Poor shielding or connectors can cause ingress/interference"),
("CATV & Satellite","Trunk Cable / Hardline Cable","Rigid/semi-rigid or corrugated coaxial trunk; often high shielding and low loss","Impedance, diameter, passive-intermodulation and connector family are system-specific","Temperature depends on jacket, connector and installation","CATV headends, distribution trunks, RF infrastructure","Low loss and robust shielding in suitable designs","Special tools/connectors; costly; less flexible"),
("CATV & Satellite","VHF Leaky Feeder Cable","Coaxial cable designed to radiate/receive controlled RF along its length","Frequency band, coupling loss and attenuation are critical","Datasheet and installation environment determine rating","VHF radio coverage in tunnels, mines and enclosed routes","Can provide distributed radio coverage where antennas are difficult","Needs engineered RF design; loss and coupling vary with frequency and surroundings"),
("CATV & Satellite","CT Coaxial Cable","Vendor/region-specific coax designation","Verify full part number, impedance and electrical data","Manufacturer datasheet required","Matching CATV/RF systems after verification","May match existing plant","Name alone is not a universal standard"),
("CATV & Satellite","KX Coaxial Cable","Coaxial family designation used in some markets; exact construction varies","Confirm impedance, shielding, attenuation and jacket","Manufacturer datasheet required","Compatible RF/CATV systems","Can suit regional installation conventions","Do not assume equivalence with RG types"),
("CATV & Satellite","VATC Coaxial Cable","European-style 75-ohm coax family designation; construction varies by grade","Confirm attenuation, shielding, CPR/jacket and conductor","Manufacturer datasheet required","TV/CATV distribution","Established product family in some markets","Exact grade and compliance must be checked"),
("CATV & Satellite","PK75 Coaxial Cable","75-ohm coaxial family/market designation","Verify attenuation, shielding, impedance and connector compatibility","Manufacturer datasheet required","Compatible video/RF distribution systems","May fit regional systems","Specifications vary by manufacturer"),
("RF Coaxial","RF Corrugated Coax Cable","Corrugated outer conductor coax; often low-loss and high shielding","Impedance (commonly 50 Ω in telecom), frequency, attenuation and PIM are critical","Depends on jacket and connector system; outdoor models available","Cellular base stations, RF feeders, antenna systems","Low loss; good shielding; rugged outdoor options","Large bend radius; connector workmanship is critical"),
("RF Coaxial","D-FB Coax Cable","Vendor/market family designation; construction varies","Require exact datasheet for impedance, attenuation and frequency","Unknown without exact product specification","RF systems where the specific D-FB type is specified","May be optimized for a particular RF installation","Name is not sufficient to determine ratings"),
("RF Coaxial","RG MIL-C-17 Cable","RG/military specification coaxial cable family; variants differ widely","Impedance, frequency, shielding and environmental qualification depend on exact M17/part number","Part-number-specific","Military, aerospace, instrumentation and RF where approved","Traceable specification may aid procurement","Many variants are not interchangeable; obsolete or superseded types possible"),
("RF Coaxial","LLC Cable","Low-loss coaxial cable family/market label; exact construction varies","Check impedance, frequency attenuation, shielding and bend radius","Manufacturer datasheet required","RF feeder and signal distribution where matched to design","Low-loss versions can support longer runs","Acronym alone is ambiguous; validate part number"),
("RF Coaxial","Leaky Coaxial Cable","Coax with controlled coupling apertures/slots for distributed RF","Coupling loss, attenuation, frequency and spacing are design parameters","Environment and jacket dependent","Tunnels, railways, mines, underground radio coverage","Distributed coverage along a route","Needs site-specific RF planning; costly compared with ordinary coax"),
("RF Coaxial","PTFE-FEP Coaxial Cable","Fluoropolymer insulation/jacket variants; often suited to demanding thermal/chemical environments","Check impedance, voltage, frequency, temperature and smoke/toxicity requirements","Some designs support roughly -55 to +200°C or higher, but exact construction governs","RF test equipment, aerospace, industrial and high-temperature routing","Good thermal/chemical performance in suitable grades","Higher cost; stiffness and termination needs vary; temperature claims must be verified"),
("Voice, Audio & Video","Voice Cable","Multi-pair copper cable for analog voice/low-rate signaling","Pair count, conductor gauge, balance and screen depend on design","Common PVC versions often around -20 to +70°C","Telephony, intercoms and low-rate signals","Simple and economical","Limited bandwidth/distance compared with modern data/fiber systems"),
("Voice, Audio & Video","Audio Video Cable Products","Umbrella family including analog/digital audio and video interconnects","Match impedance, shielding, connector and signal format","Product-specific","AV equipment, studios, conferencing and media systems","Many formats available","Generic label is not a specification; mismatched cable can impair signal"),
("Voice, Audio & Video","5.5 Parallel Speaker Cable","Two parallel insulated conductors","Conductor cross-section and run length set resistance/voltage drop","Common PVC products often around -20 to +70°C","Loudspeaker connections","Low cost; easy to install","Unshielded; polarity and gauge matter; not a signal/data cable"),
("Voice, Audio & Video","5.4 Multicore Circular Speaker Cable","Multiple insulated speaker conductors in round jacket","Core count and cross-section vary","Product-specific, often ambient indoor range","Multi-zone audio, stage and installed sound","Neat multi-channel routing","Larger/heavier than parallel cable; label cores carefully"),
("Voice, Audio & Video","5.3 Circular Shielded Audio Cable","Shielded balanced/unbalanced audio conductors in circular jacket","Conductor count, screen coverage and capacitance matter","Product-specific; commonly indoor PVC range","Microphones, line-level audio, studios and live sound","Shield reduces electromagnetic interference","Shield/grounding errors can create hum; not intended for speaker power unless rated"),
("Voice, Audio & Video","5.6 Media Composite Cable","Combined cable for multiple media signals, often video/audio/control or power","Exact signal formats and impedance must be checked","Product-specific","AV racks, broadcast and integrated media systems","Reduces cable bundles","One jacket may constrain routing; mixed signals require compatibility checks"),
("Voice, Audio & Video","5.2 Audio Speaker Cable","Two or more conductors sized for loudspeaker current","Cross-section, conductor material and length determine losses","Common PVC types often around -20 to +70°C","Passive loudspeakers, amplifiers and installed audio","Simple, low-cost, easy to terminate","No inherent shielding; undersized cable causes losses/heating"),
("Voice, Audio & Video","5.1 Flat Telephone Cable","Flat multi-conductor telephone lead, often stranded","Pinout, conductor count and connector type are important","Typical indoor use; verify product data","Telephone handset/line patching and legacy connections","Flexible and compact","Limited mechanical protection; not suitable for outdoor or high-power use"),
("Control & Instrumentation","6.1 Flex Control Cable","Flexible multi-core control cable; PVC/TPE/other jackets depending on grade","Voltage, core count, flexing class, shielding and oil resistance vary","Common PVC types often -5/-20 to +70°C; moving-duty grades differ","Machinery, panels, automation and control circuits","Flexible; many construction options","Continuous-flex performance is not universal; EMC and bend radius need checking"),
("Control & Instrumentation","6.2 Sensor & Actuator Cable – Zion","Industrial sensor/actuator cable; connectorized or cut-length options may exist","Check pinout, conductor size, IP rating, shield and chemical resistance","Product-specific; verify vendor datasheet","Proximity sensors, actuators, industrial I/O","Designed for automation connectivity","Connector and environment ratings are system-specific"),
("Control & Instrumentation","6.6 Marine LAN Cable – Zion","LAN cable for marine environments; shielding/jacket and approvals vary","Category, impedance, flame/smoke, oil/saltwater and marine approvals need verification","Product-specific; marine-grade does not imply a universal temperature range","Shipboard networks and marine automation","Can be specified for harsh marine settings","Must verify marine type approval, fire performance and installation rules"),
("Power & Energy","7.1 Solar Cable – Zion","PV cable typically uses UV/ozone/weather-resistant insulation and flexible copper conductors","DC voltage rating, conductor size, UV/ozone, wet-location and connector compatibility","Many PV cables are rated around -40 to +90°C ambient, with conductor max often 90/120°C; confirm exact datasheet","PV module strings, DC combiner and inverter connections","UV/weather resistance; designed for PV service","Connector compatibility and DC isolation are safety-critical; not all outdoor cable is PV-rated"),
("Power & Energy","7.2 Battery Cable – Zion","Flexible, often fine-stranded copper cable with durable insulation","Ampacity depends on cross-section, installation, ambient temperature and duty cycle","Product-specific; automotive/battery grades differ","Battery banks, inverters, UPS and DC systems","Flexible; handles high-current DC when correctly sized","High fault currents; correct fuse, lug crimping and voltage-drop design are essential"),
("Power & Energy","7.3 General Power Cable – Zion","Power cable family with conductor/insulation options","Voltage class, conductor material, insulation and installation method govern selection","Manufacturer and standard-specific","Equipment feeds and general power distribution within rated scope","Broad range of constructions","Generic family name cannot establish voltage or ampacity"),
("Power & Energy","7.4 KNX Cable – Zion","Typically twisted-pair bus cable, often green jacket in common KNX installations","Bus topology, conductor pair, capacitance and certification are relevant","Often around -5 to +70°C for common products; verify exact cable","Building automation, KNX sensors, actuators and controllers","Purpose-built bus wiring; low data rate control network","Not a substitute for mains cable; observe separation and topology rules"),
("Power & Energy","7.5 LV Armoured Cable SWA & AWA – Zion","Low-voltage power cable with steel wire armour (SWA) or aluminium wire armour (AWA), depending on design","Conductor size, cores, voltage, armour, gland and fault-current requirements","Common XLPE designs may have 90°C conductor limit; PVC/ambient ratings differ","Buried, outdoor and mechanically exposed LV distribution where approved","Mechanical protection; suitable for demanding routes when correctly selected","Heavy and less flexible; glands/earthing and burial conditions matter"),
("Power & Energy","7.6 Automotive Cable – Zion","Automotive wire/cable with insulation suited to vehicle vibration, fluids and temperature","Automotive standard, conductor size, voltage and fluid resistance vary","Some automotive grades operate around -40 to +105°C or more; exact type governs","Vehicle wiring, harnesses, sensors and accessories","Flexible; designed for vehicle environments","Not automatically suitable for building wiring; routing and abrasion protection matter"),
("Power & Energy","7.7 High Temperature Cable – Zion","Special insulation such as silicone, fluoropolymer or glass-fibre systems depending on type","Temperature, voltage, chemical resistance and flex life are construction-specific","Could range from about +150°C to +250°C or more for some types; never assume without datasheet","Furnaces, heaters, industrial equipment and hot zones","Supports elevated-temperature service in appropriate grades","Costlier; temperature rating may depend on continuous vs short-term exposure and installation"),
("LAN / Ethernet","LAN/Ethernet Cable Products Catalog","Twisted-pair balanced copper cable (Cat5e/Cat6/Cat6A and other grades)","Category, bandwidth, length, shielding, conductor gauge and PoE bundle heating","Common indoor PVC types often around 0 to +60°C installation/operation ranges; check cable data","Ethernet LANs, office networks, IP cameras, access points","Easy termination; high-speed networking; PoE options","Copper channel length typically 100 m; EMI, bend radius and PoE heating matter"),
("LAN / Ethernet","Copper Patch Cord","Factory-terminated twisted-pair Ethernet cord","Category, length, stranded conductor, connector and PoE rating","Product-specific; usually indoor ambient range","Switch-to-device and patch-panel connections","Quick deployment; reduced field-termination effort","Patch cords add channel length; poor-quality cords can limit performance"),
("LAN / Ethernet","LAN/Ethernet Cable – Customized Types","Custom category, shielding, jacket, color or conductor design","Requires exact approved drawing and datasheet","Customer-specific","Special network installations","Can match project needs","Long lead times; verify performance with certification testing"),
("LAN / Ethernet","LAN/Ethernet Cable – Ethernet Plenum Cable","Cable with jacket/materials suitable for designated air-handling spaces under applicable code","Category plus required plenum/fire-smoke compliance (e.g., local CMP/CPR equivalents)","Product-specific; plenum rating is not a temperature rating","Plenum/air-handling spaces where code requires it","Can satisfy specific fire/smoke installation rules","More expensive; regional classifications are not interchangeable"),
("Fiber Optic","1. ADSS Optical Fiber Cable","All-dielectric self-supporting aerial fiber cable","Span, wind/ice loading, sag-tension, fiber count and electrical field exposure must be engineered","Manufacturer-specific; outdoor range often broad, e.g. -40 to +70°C","Aerial telecom routes near power infrastructure where designed","No metallic strength member; self-supporting","Span and loading design critical; not every ADSS fits every voltage/route"),
("Fiber Optic","2. FTTH Drop Optical Fiber Cable","Compact drop fiber with strength members and bend-optimized fiber options","Fiber type, bend radius, tensile load and connectorization","Product-specific; indoor/outdoor ratings differ","Last-mile fiber-to-the-home connections","Compact; supports high bandwidth","Fragile compared with copper; bend and pulling limits matter"),
("Fiber Optic","3. Aerial Installation Optical Fiber Cable Figure-8 Self-supporting","Fiber cable with messenger wire in figure-8 profile","Span, messenger strength, wind/ice load and sag limits","Outdoor rating per datasheet","Aerial access and distribution networks","Convenient aerial installation","Heavier/visible; messenger bonding/handling requirements"),
("Fiber Optic","4. Duct Installation Optical Fiber Cable Light Armor","Duct-rated fiber with light armor for added protection","Fiber count, tensile/crush resistance, duct and water-blocking design","Product-specific outdoor range","Ducted telecom routes","Extra protection compared with unarmored duct cable","Armor increases size/cost; pulling tension limits still apply"),
("Fiber Optic","5. Direct Buried Optical Fiber Cable Double Sheath Enhanced Armor","Fiber cable with double sheath and enhanced armor for direct burial","Crush/impact, water blocking, burial depth and soil/rodent conditions","Product-specific; verify direct-burial approval","Direct-buried backbone/access networks","Strong mechanical and moisture protection","More expensive and harder to repair; installation practice matters"),
("Fiber Optic","6. Air-Blown Micro Optical Fiber Cable for FTTx","Small-diameter microcable designed for blowing into microducts","Duct compatibility, blowing distance, pressure, fiber count and bend radius","Manufacturer-specific","FTTx networks using microduct infrastructure","Fast additions/upgrades; high duct utilization","Needs compatible ducts and blowing equipment"),
("Fiber Optic","7. Optical Fiber Cable for Cabling in Buildings","Indoor fiber cable with tight/loose tube or breakout construction","Fiber type, fire/smoke class, bend radius and connector requirements","Indoor rating per datasheet","Building backbone, risers, horizontal fiber links","High bandwidth; immune to electromagnetic interference","Requires optical transceivers and careful termination"),
("Fiber Optic","8. Optical Fiber Cable for Networks in Rural Areas","Outdoor fiber designed for long rural access routes","Span/duct/burial method, water blocking, fiber count and environmental design","Manufacturer-specific","Rural broadband and long-distance access","Scalable reach; low signal loss over distance","Civil works and repair logistics can be costly"),
("Fiber Optic","9. Optical Cable for Route Shortage (catalog label)","Vendor-specific label; likely a special route/space constraint design but exact construction is unclear","Request full part number and technical datasheet","Unknown until identified","Only after vendor confirms intended application","Could address a specific routing constraint","Name alone is ambiguous; do not infer installation or performance"),
("Fiber Optic","10. Optical Cables for Distributed Base Stations","Fiber cable for distributed radio/base-station architecture; hybrid or all-dielectric options possible","Fiber count, remote radio architecture, environmental and connector requirements","Product-specific","Mobile network base stations, distributed antenna/radio systems","High-capacity, low-loss digital transport","System architecture and connector compatibility must be checked"),
("Fiber Optic","11. Biological Protection Optical Fiber Cable (anti-rodent/termite/birds)","Cable with selected barriers, armor or materials to mitigate specified biological damage","Protection method, environment, armor and installation type are product-specific","Manufacturer-specific","Routes exposed to rodents, termites or birds, where tested design is suitable","Can reduce biological damage risk","No cable is universally animal-proof; validate test method and local hazards"),
("Fiber Optic","12. Fire-Resistance Optical Fiber Cable for Railway Transportation","Railway-oriented fiber construction with fire/smoke/toxicity or circuit survival properties depending on product","Railway approvals, fire performance, smoke/toxicity, mechanical and circuit requirements","Specific railway datasheet and approval required","Railway communications, signaling or rolling-stock infrastructure as approved","Can be designed for demanding rail safety requirements","Fire reaction, fire resistance and functional survival are distinct; approvals are essential"),
("Fiber Optic","Outdoor Optical Fiber Cable","Outdoor-rated fiber construction, often water-blocked and UV-resistant","Installation type, fiber count, tensile/crush rating and jacket","Product-specific outdoor range","Outdoor telecom links","EMI immunity; high bandwidth; long reach","Correct construction needed for aerial/duct/buried installation"),
("Fiber Optic","Indoor Optical Fiber Cable","Indoor cable construction selected for building routes","Fiber type, bend radius and fire/smoke classification","Indoor datasheet and local code govern","Building risers, horizontal and backbone networks","Compact; high bandwidth; no EMI pickup","Fire classification and routing rules matter; fiber handling/cleanliness needed"),
("Fiber Optic","Spiral Steel Pipe","Likely spiral steel conduit/pipe associated with cable protection; confirm catalog intent","Material, diameter, corrosion protection and mechanical rating required","Not a cable operating-temperature rating; use pipe/coating data","Mechanical protection or cable routing where specified","Can offer mechanical protection","Item identity is ambiguous; not an optical fiber cable specification"),
("Fiber Optic","Round Ribbon Fiber Cable","Fiber ribbon arrangement within a round cable profile","Fiber count, ribbon design, mass-fusion splice compatibility and bend radius","Product-specific","High-count backbone/data-center/telecom routes","High fiber density; efficient mass fusion splicing","Specialized splicing tools; bend/handling limits"),
("Fiber Optic","Flat Fiber Ribbon Cable","Flat ribbon arrangement of multiple optical fibers","Fiber count, ribbon construction, splice and bend limits","Product-specific","High-density optical distribution and mass splicing","Dense, organized fiber layout","May be less suitable for some tight routes; protect against kinking"),
("Fiber Optic","Hybrid Fiber Copper – Stranded","Hybrid cable combines optical fibers with copper conductors; stranded version depends on design","Fiber count, copper voltage/current, isolation and environmental rating","Product-specific; separate fiber and copper limits apply","Remote radio units, industrial systems and combined data/power routes","Combines data and power in one route","Electrical and optical safety/termination requirements coexist; size carefully"),
("Fiber Optic","EPFU Enhanced Performance Fibre Units Air-Blown Micro Optical Fiber Cable for FTTx","Enhanced-performance fiber unit intended for air-blown microduct installation","Duct size, blowing pressure/distance, fiber count and bend radius","Manufacturer-specific","FTTx upgrades and microduct networks","Flexible network expansion without replacing main ducts","Requires matched duct system and installation equipment"),
]

base_columns = ["Category", "Cable / Product", "Characteristics", "Key specifications to verify", "Indicative operating temperature", "Typical applications", "Pros", "Cons"]
evidence_columns = [
    "Manufacturer", "Exact model / part number", "Certified operating temperature range",
    "Temperature rating type", "Applicable standard", "Certificate / DoP ID",
    "Certification body", "Datasheet URL", "Certificate URL", "Image URL", "Verification status",
    "Verification notes"
]
columns = base_columns + evidence_columns

df_default = pd.DataFrame(CATALOG, columns=base_columns)
# Never convert generic family estimates into certified values. Certification is product-specific.
for col in evidence_columns:
    df_default[col] = ""
df_default["Verification status"] = "Unverified — exact manufacturer evidence required"

@st.cache_data
def make_csv(data):
    return data.to_csv(index=False).encode("utf-8")

def clean_text(value):
    if pd.isna(value):
        return ""
    return str(value).strip()

def valid_http_url(value):
    value = clean_text(value)
    return value.startswith("https://") or value.startswith("http://")

def category_image_path(category_name):
    slug = re.sub(r"[^a-z0-9]+", "_", clean_text(category_name).lower()).strip("_")
    return Path(__file__).parent / "cable_images" / f"{slug}.png"

with st.sidebar:
    st.header("Explore the catalog")
    st.caption("Filter the cable families, add manufacturer evidence, and attach product snapshots.")
    uploaded = st.file_uploader("Upload cable catalog (CSV)", type=["csv"])
    if uploaded:
        try:
            user_df = pd.read_csv(uploaded).fillna("")
            missing = [c for c in base_columns if c not in user_df.columns]
            if missing:
                st.error("CSV is missing required base columns: " + ", ".join(missing))
                st.caption("Download the expanded template below to see every supported field.")
                data = df_default.copy()
            else:
                for col in evidence_columns:
                    if col not in user_df.columns:
                        user_df[col] = ""
                data = user_df[columns].copy()
                st.success(f"Loaded {len(data)} cable records.")
        except Exception as e:
            st.error(f"Could not read CSV: {e}")
            data = df_default.copy()
    else:
        data = df_default.copy()
    categories = ["All categories"] + sorted(data["Category"].dropna().astype(str).unique().tolist())
    category = st.selectbox("Cable family", categories)
    search = st.text_input("Search cable name, standard, manufacturer or application")
    only_named = st.checkbox("Show only records with complete product names", value=False)
    only_verified = st.checkbox("Show only records with manufacturer evidence marked verified", value=False)

if category != "All categories":
    view = data[data["Category"] == category].copy()
else:
    view = data.copy()
if search.strip():
    q = search.strip().lower()
    mask = view.astype(str).apply(lambda col: col.str.lower().str.contains(q, na=False)).any(axis=1)
    view = view[mask]
if only_named:
    view = view[~view["Cable / Product"].astype(str).str.contains("incomplete|ambiguous|catalog label", case=False, na=False)]
if only_verified:
    view = view[view["Verification status"].astype(str).str.contains(r"verified|checked", case=False, na=False)]

m1, m2, m3, m4 = st.columns(4)
m1.metric("Catalog entries", f"{len(data):,}")
m2.metric("Cable families", f"{data['Category'].nunique():,}")
m3.metric("Current results", f"{len(view):,}")
verified_count = data["Verification status"].astype(str).str.contains(r"verified|checked", case=False, na=False).sum()
m4.metric("Evidence-verified records", f"{verified_count:,}")

st.info(
    "Certification safeguard: the catalog's family-level temperature estimates are not certified ratings. "
    "A certified range can only be recorded when it is tied to an exact manufacturer, model/part number, "
    "rating type and traceable datasheet/certificate. Generic cable names alone do not establish certification."
)

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📚 Cable catalog", "🔎 Compare cables", "🖼️ Snapshots & details", "📥 Upload & export", "🧭 Selection guide"
])

with tab1:
    st.subheader("Cable family reference")
    if view.empty:
        st.warning("No cable records match those filters.")
    else:
        show_cols = ["Category", "Cable / Product", "Indicative operating temperature", "Certified operating temperature range", "Verification status"]
        st.dataframe(view[show_cols], use_container_width=True, hide_index=True)
        st.caption("Use the Snapshots & details tab to inspect product images and evidence fields.")

with tab2:
    st.subheader("Side-by-side comparison")
    options = view["Cable / Product"].astype(str).drop_duplicates().tolist()
    selected = st.multiselect("Select 2–4 cables", options, default=options[:2] if len(options) >= 2 else options, max_selections=4)
    if selected:
        comp = view[view["Cable / Product"].astype(str).isin(selected)].drop_duplicates("Cable / Product")
        compare_cols = base_columns + ["Manufacturer", "Exact model / part number", "Certified operating temperature range", "Temperature rating type", "Applicable standard", "Certificate / DoP ID", "Datasheet URL", "Verification status"]
        st.dataframe(comp[compare_cols].set_index("Cable / Product").T, use_container_width=True)
    else:
        st.caption("Select at least one cable to compare.")

with tab3:
    st.subheader("Cable snapshots and interactive product details")
    with st.expander("Browse all cable-category visuals", expanded=True):
        gallery_categories = sorted(data["Category"].dropna().astype(str).unique().tolist())
        for start in range(0, len(gallery_categories), 5):
            gallery_cols = st.columns(5)
            for j, cat_name in enumerate(gallery_categories[start:start + 5]):
                with gallery_cols[j]:
                    visual = category_image_path(cat_name)
                    if visual.exists():
                        st.image(str(visual), caption=cat_name, use_container_width=True)
                    else:
                        st.caption(cat_name + " — image not available")
    st.caption("Built-in category visuals are illustrations. Add product-specific official images through the Image URL field or upload a snapshot for the current session.")
    if view.empty:
        st.warning("No cable records match those filters.")
    else:
        choice = st.selectbox("Choose a cable", view["Cable / Product"].astype(str).tolist(), key="detail_choice")
        row = view[view["Cable / Product"].astype(str) == choice].iloc[0]
        st.markdown(f"### {choice}")
        st.caption(f"{clean_text(row['Category'])} · {clean_text(row['Manufacturer']) or 'Manufacturer not specified'}")
        image_url = clean_text(row.get("Image URL", ""))
        left, right = st.columns([1, 1.4])
        with left:
            if valid_http_url(image_url):
                try:
                    st.image(image_url, caption=f"Product snapshot: {choice}", use_container_width=True)
                except Exception:
                    st.warning("The image URL could not be displayed. Check that it is a direct, publicly accessible image URL.")
            else:
                illustration = category_image_path(row["Category"])
                if illustration.exists():
                    st.image(str(illustration), caption=f"{row['Category']} — illustrative reference, not a product photo", use_container_width=True)
                st.info("No product-specific snapshot is attached yet. Add an official manufacturer image URL in the CSV, or upload a snapshot below for this session.")
            snap = st.file_uploader("Upload a cable snapshot (PNG/JPG/JPEG/WebP)", type=["png", "jpg", "jpeg", "webp"], key=f"snap_{choice}")
            if snap is not None:
                st.image(snap, caption=f"Uploaded reference snapshot — {choice}", use_container_width=True)
                st.caption("This uploaded image is displayed for this session only; add its public image URL to the CSV to include it in future deployments.")
        with right:
            st.markdown("#### Engineering details")
            detail_groups = [
                ("Characteristics", "Characteristics"),
                ("Specifications to verify", "Key specifications to verify"),
                ("Indicative family temperature (not certified)", "Indicative operating temperature"),
                ("Applications", "Typical applications"),
                ("Advantages", "Pros"),
                ("Limitations", "Cons"),
            ]
            for label, col in detail_groups:
                with st.expander(label, expanded=(label == "Characteristics")):
                    st.write(clean_text(row[col]) or "Not provided in this record.")
        st.markdown("#### Manufacturer certification and traceability")
        evidence_fields = [
            ("Manufacturer", "Manufacturer"), ("Exact model / part number", "Exact model / part number"),
            ("Certified operating temperature range", "Certified operating temperature range"),
            ("Temperature rating type (operating / installation / conductor / short-circuit)", "Temperature rating type"),
            ("Applicable standard", "Applicable standard"), ("Certificate / Declaration of Performance ID", "Certificate / DoP ID"),
            ("Certification body", "Certification body"), ("Verification status", "Verification status"),
            ("Verification notes", "Verification notes")
        ]
        evidence_cols = st.columns(3)
        for i, (label, col) in enumerate(evidence_fields):
            with evidence_cols[i % 3]:
                st.markdown(f"**{label}**")
                st.write(clean_text(row.get(col, "")) or "Not supplied — do not treat as certified.")
        link_cols = st.columns(2)
        datasheet = clean_text(row.get("Datasheet URL", ""))
        cert_url = clean_text(row.get("Certificate URL", ""))
        with link_cols[0]:
            if valid_http_url(datasheet):
                st.link_button("Open manufacturer datasheet", datasheet)
        with link_cols[1]:
            if valid_http_url(cert_url):
                st.link_button("Open certificate / DoP", cert_url)
        if not clean_text(row.get("Certified operating temperature range", "")) or not valid_http_url(datasheet):
            st.warning("Certification evidence is incomplete. Do not describe this record's temperature range as certified until the exact product datasheet and relevant certificate/DoP are checked.")

with tab4:
    st.subheader("Upload evidence, snapshots and export")
    st.write("Upload a CSV with product-specific evidence fields. Optional columns can include manufacturer, part number, certified temperature range, rating type, standard, certificate/DoP ID, certification body, datasheet URL, certificate URL, image URL, verification status and notes.")
    st.markdown("**Required base columns**")
    st.code(", ".join(base_columns))
    st.markdown("**Additional evidence and image columns**")
    st.code(", ".join(evidence_columns))
    st.download_button("Download complete catalog CSV", data=make_csv(df_default), file_name="cable_catalog.csv", mime="text/csv")
    st.download_button("Download expanded blank template CSV", data=make_csv(pd.DataFrame(columns=columns)), file_name="cable_catalog_template.csv", mime="text/csv")
    st.download_button("Export current results CSV", data=make_csv(view), file_name="cable_catalog_filtered.csv", mime="text/csv")
    st.caption("CSV uploads and uploaded snapshots are session-only. To make them permanent, update the catalog/image URLs in the GitHub repository and redeploy.")

with tab5:
    st.subheader("Practical selection checklist")
    st.markdown("""
1. **Define the service:** power, RF, Ethernet, optical fiber, control, audio/video, security or life-safety.
2. **Confirm electrical/optical requirements:** voltage, current, impedance, frequency, attenuation, bandwidth, conductor size, fiber count and voltage drop.
3. **Match installation conditions:** indoor/outdoor, direct burial, duct, aerial span, UV, moisture, oil, chemicals, vibration, rodents and bend radius.
4. **Identify the temperature rating type:** ambient operating, conductor maximum, installation, storage or short-circuit rating are not interchangeable.
5. **Verify fire requirements:** reaction-to-fire classification, smoke/halogen performance and circuit integrity/fire resistance are different properties.
6. **Check the exact evidence:** manufacturer, full part number, datasheet revision, certificate/DoP scope, test standard, jurisdiction and certificate validity.
7. **Document the decision:** installation method, length, derating, connectors, termination, inspection and test results.
""")
    st.warning("Do not select fire alarm, mains power, PV DC, battery or railway cable solely from a generic family reference. Use a qualified engineer and the applicable code.")

st.divider()
st.caption("Prepared by Engr. Syed Hassan Iqbal Shah · Generic family-level data is indicative only. No entry is manufacturer-certified unless exact, traceable product evidence is supplied and verified.")
