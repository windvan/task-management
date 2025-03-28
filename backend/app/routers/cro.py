from fastapi import APIRouter, status, HTTPException, Body
from sqlmodel import select, or_

from ..schemas.cro import Cro, CroCreate, CroPublic, CroUpdate, CroContact, CroContactCreate, CroContactPublic, CroContactUpdate
from ..utils.dependencies import SessionDep, TokenDep

router = APIRouter(prefix='/cros', tags=["CRO"])


# region CRO
@router.post('/', response_model=CroPublic, status_code=status.HTTP_201_CREATED)
def create_cro(cro_create: CroCreate, session: SessionDep):
    print('\n\n\n\n\n cro_create:', cro_create)
    db_cro = Cro.model_validate(cro_create)
    session.add(db_cro)

    try:
        session.commit()
        session.refresh(db_cro)
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))

    return db_cro


@router.get('/', response_model=list[CroPublic])
def get_cros(session: SessionDep):
    db_cros = session.exec(select(Cro)).all()
    return db_cros


@router.get('/search')
def search_cros(session: SessionDep,  query: str = ""):
    search_pattern = f"%{query}%"
    conditions = or_(
        Cro.address.ilike(search_pattern),
        Cro.certification_number.ilike(search_pattern),
        Cro.cro_name.ilike(search_pattern),
    )
    stmt = select(
        Cro.id,
        Cro.cro_name,
    ).where(conditions)
    db_cros = session.exec(stmt).mappings().all()
    return db_cros


@router.patch('/{cro_id}', response_model=CroPublic)
async def update_cro(cro_id: int, cro_update: CroUpdate, session: SessionDep):
    db_cro = session.get(Cro, cro_id)
    if not db_cro:
        raise HTTPException(status_code=404, detail="Cro not found")

    cro_data = cro_update.model_dump(exclude_unset=True)
    db_cro.sqlmodel_update(cro_data)
    session.add(db_cro)
    session.commit()
    session.refresh(db_cro)
    return db_cro


@router.delete("/{cro_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cro(cro_id: int, session: SessionDep):
    db_cro = session.get(Cro, cro_id)
    if not db_cro:
        raise HTTPException(status_code=404, detail="Cro not found")
    session.delete(db_cro)
    session.commit()
    return {"message": "CRO deleted successfully"}


@router.get('/{cro_id}', response_model=CroPublic)
async def get_cro(cro_id: int, session: SessionDep):
    db_cro = session.get(Cro, cro_id)

    if not db_cro:
        raise HTTPException(status_code=404, detail="Cro not found")

    return db_cro


# endregion

# region CRO contact


@router.post('/contacts', response_model=CroContactPublic, status_code=status.HTTP_201_CREATED)
def create_cro_contact(contact_create: CroContactCreate, session: SessionDep):
    db_contact = CroContact.model_validate(contact_create)
    session.add(db_contact)

    try:
        session.commit()
        session.refresh(db_contact)
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    return db_contact


@router.get('/contacts/{contact_id}', response_model=CroContactPublic)
def get_cro_contact(contact_id: int, session: SessionDep):
    # get single contact by id
    db_contact = session.get(CroContact, contact_id)

    if not db_contact:
        raise HTTPException(status_code=404, detail="Contact not found")

    return db_contact


@router.get('/contacts', response_model=list[CroContactPublic])
def get_cro_contacts(session: SessionDep):
    db_contacts = session.exec(select(CroContact)).all()
    return db_contacts


@router.patch('/contacts/{contact_id}', response_model=CroContactPublic)
def update_cro_contact(contact_id: int, contact_update: CroContactUpdate, session: SessionDep):
    db_contact = session.get(CroContact, contact_id)
    if not db_contact:
        raise HTTPException(status_code=404, detail="Cro not found")

    contact_data = contact_update.model_dump(exclude_unset=True)
    db_contact.sqlmodel_update(contact_data)
    session.add(db_contact)
    session.commit()
    session.refresh(db_contact)
    return db_contact


@router.delete("/contacts/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cro_contact(contact_id: int, session: SessionDep):
    db_contact = session.get(CroContact, contact_id)
    if not db_contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    session.delete(db_contact)
    session.commit()
    return {"message": "CRO contact deleted successfully"}


@router.get('/{cro_id}/contacts', response_model=list[CroContactPublic])
def get_cro_contact(cro_id: int, session: SessionDep):
    # get all contacts related to a cro
    db_contacts = session.exec(select(CroContact).where(
        CroContact.cro_id == cro_id)).all()
    # print(db_contacts)
    # if not db_contacts:
    #     raise HTTPException(status_code=404, detail="Cro contacts not found")

    return db_contacts
# endregion
