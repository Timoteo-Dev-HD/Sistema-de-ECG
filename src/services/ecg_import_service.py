import os
from src.settings.extensions import db
from src.models.ecg_exams_model import EcgExam
from src.models.paciente_model import Paciente, SexoEnum
from src.utils.zoncare_xml import parse_zoncare_xml

ECG_DIR = "ecg_local"


def import_local_ecgs():
    files = os.listdir(ECG_DIR)
    xml_files = [f for f in files if f.endswith(".xml")]

    for xml_file in xml_files:

        pdf_file = xml_file.replace(".xml", ".pdf")

        if EcgExam.query.filter_by(arquivo=pdf_file).first():
            continue

        xml_path = os.path.join(ECG_DIR, xml_file)
        data = parse_zoncare_xml(xml_path)

        patient_data = data["patient"]

        paciente = Paciente.query.filter_by(
            external_id=patient_data["external_id"]
        ).first()

        sexo_enum = None
        if patient_data["gender"] == "M":
            sexo_enum = SexoEnum.MASCULINO
        elif patient_data["gender"] == "F":
            sexo_enum = SexoEnum.FEMININO

        if not paciente:
            paciente = Paciente(
                external_id=patient_data["external_id"],
                nome=patient_data["name"],
                idade=int(patient_data["age"]) if patient_data["age"] else None,
                idade_unidade=patient_data["age_unit"],
                sexo=sexo_enum,
                setor=patient_data["department"],
                leito=patient_data["bed"],
                peso_kg=float(patient_data["weight"]) if patient_data["weight"] else None,
                altura_cm=float(patient_data["height"]) if patient_data["height"] else None,
            )
            db.session.add(paciente)
            db.session.flush()
        else:
            # Atualiza dados caso mudem
            paciente.nome = patient_data["name"]
            paciente.idade = int(patient_data["age"]) if patient_data["age"] else None
            paciente.idade_unidade = patient_data["age_unit"]
            paciente.sexo = sexo_enum
            paciente.setor = patient_data["department"]
            paciente.leito = patient_data["bed"]
            paciente.peso_kg = float(patient_data["weight"]) if patient_data["weight"] else None
            paciente.altura_cm = float(patient_data["height"]) if patient_data["height"] else None

        exam = EcgExam(
            paciente_id=paciente.id,
            frequencia_media=data["measures"]["hr"],
            arquivo=pdf_file,
            observacoes=data["report"]["advicetext"],
            created_by=1
        )

        db.session.add(exam)
        db.session.commit()