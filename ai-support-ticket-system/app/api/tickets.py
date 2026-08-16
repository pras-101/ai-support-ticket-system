from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db_session
from app.models.ticket import Ticket
from app.models.user import User, UserRole
from app.schemas.ticket import TicketCreate, TicketRead
from app.services.auth import get_current_user, require_roles

router = APIRouter(prefix="/tickets", tags=["tickets"])


@router.post("", response_model=TicketRead, status_code=status.HTTP_201_CREATED)
async def create_ticket(
    ticket_in: TicketCreate,
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(require_roles(UserRole.CUSTOMER)),
) -> Ticket:
    ticket = Ticket(**ticket_in.model_dump(), customer_id=current_user.id)
    session.add(ticket)
    await session.commit()
    await session.refresh(ticket)
    return ticket


@router.get("", response_model=list[TicketRead])
async def list_tickets(
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
) -> list[Ticket]:
    query = select(Ticket).order_by(Ticket.created_at.desc())
    if current_user.role == UserRole.CUSTOMER:
        query = query.where(Ticket.customer_id == current_user.id)
    result = await session.scalars(query)
    return list(result)


@router.get("/{ticket_id}", response_model=TicketRead)
async def get_ticket(
    ticket_id: int,
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
) -> Ticket:
    ticket = await session.get(Ticket, ticket_id)
    if ticket is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")
    if current_user.role == UserRole.CUSTOMER and ticket.customer_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You cannot access this ticket")
    return ticket
