from sqlalchemy.orm import Session

from app.models.voting_system_config_model import VotingConfigModel, VotingStatus


def get_voting_config(db: Session) -> VotingConfigModel:
    """
    Get voting config from DB.
    If not exists → create it automatically.
    """
    config = db.query(VotingConfigModel).first()

    if not config:
        config = VotingConfigModel()
        db.add(config)
        db.commit()
        db.refresh(config)

    return config


def is_limit_reached(db: Session) -> bool:
    """
    Check if number of voters reached the configured limit.
    """
    from app.models.voter import Voter  # avoid circular import

    config = get_voting_config(db)
    count = db.query(Voter).count()

    return count >= config.num_voters


def should_send_emails(db: Session) -> bool:
    """
    True only if:
    - limit reached
    - emails not already sent
    """
    config = get_voting_config(db)
    return is_limit_reached(db) and not config.emails_sent


def mark_emails_sent(db: Session):
    """
    Mark emails as sent (prevents duplicates after restart).
    """
    config = get_voting_config(db)
    config.emails_sent = True
    db.commit()


# def reset_emails_flag(db: Session):
#     """
#     Reset flag (useful for testing or new election).
#     """
#     config = get_voting_config(db)
#     config.emails_sent = False
#     db.commit()

def emails_already_sent(db: Session) -> bool:
    config = get_voting_config(db)
    return config.emails_sent

def set_voting_started(db:Session):
    config = get_voting_config(db)
    config.voting_status = VotingStatus.VOTE_STARTED
    db.commit()
    
def set_voting_ended(db:Session):
    config = get_voting_config(db)
    config.voting_status = VotingStatus.VOTE_ENDED
    db.commit()
