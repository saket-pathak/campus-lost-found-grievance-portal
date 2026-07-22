import pytest
from datetime import date
from django.contrib.auth import get_user_model
from lostfound.models import LostItem, FoundItem, ClaimRequest
from lostfound.matching import find_potential_matches

User = get_user_model()

@pytest.mark.django_db
def test_matching_algorithm():
    user1 = User.objects.create_user(username='u1', password='p', role='student')
    user2 = User.objects.create_user(username='u2', password='p', role='student')
    
    lost = LostItem.objects.create(
        reporter=user1,
        title="Black leather wallet with keys",
        description="Lost a black leather wallet containing credit cards and room keys",
        category="electronics",
        location_lost="Library",
        date_lost=date(2026, 7, 20),
        status="open"
    )
    
    found1 = FoundItem.objects.create(
        finder=user2,
        title="Black wallet",
        description="Found a black wallet with keys inside",
        category="electronics",
        location_found="Library 2nd Floor",
        date_found=date(2026, 7, 21),
        status="unclaimed"
    )
    
    found2 = FoundItem.objects.create(
        finder=user2,
        title="Blue water bottle",
        description="Left behind on table",
        category="other",
        location_found="Cafeteria",
        date_found=date(2026, 7, 21),
        status="unclaimed"
    )
    
    matches = find_potential_matches(lost)
    assert len(matches) == 1
    assert matches[0] == found1
    assert matches[0].match_score > 50

@pytest.mark.django_db
def test_claim_flow():
    finder = User.objects.create_user(username='finder', password='p', role='student')
    claimant = User.objects.create_user(username='claimant', password='p', role='student')
    claimant2 = User.objects.create_user(username='claimant2', password='p', role='student')
    
    found = FoundItem.objects.create(
        finder=finder,
        title="Keys",
        description="Found keys on campus",
        category="keys",
        location_found="Gym",
        date_found=date(2026, 7, 20)
    )
    
    claim = ClaimRequest.objects.create(
        found_item=found,
        claimant=claimant,
        proof_description="I lost keys with a red key chain"
    )
    claim2 = ClaimRequest.objects.create(
        found_item=found,
        claimant=claimant2,
        proof_description="I lost keys with blue key chain"
    )
    
    assert found.status == 'unclaimed'
    assert claim.status == 'pending'
    
    claim.status = 'approved'
    claim.save()
    found.status = 'claimed'
    found.save()
    
    other_claims = found.claim_requests.filter(status='pending').exclude(pk=claim.pk)
    for other in other_claims:
        other.status = 'rejected'
        other.save()
        
    claim.refresh_from_db()
    claim2.refresh_from_db()
    found.refresh_from_db()
    
    assert found.status == 'claimed'
    assert claim.status == 'approved'
    assert claim2.status == 'rejected'


@pytest.mark.django_db
def test_lost_item_close():
    reporter = User.objects.create_user(username='reporter', password='p', role='student')
    staff = User.objects.create_user(username='staff', password='p', role='staff')
    other_user = User.objects.create_user(username='other_user', password='p', role='student')
    
    lost = LostItem.objects.create(
        reporter=reporter,
        title="Phone",
        description="Lost a phone",
        category="electronics",
        location_lost="Main Building",
        date_lost=date(2026, 7, 20),
        status="open"
    )
    
    from django.urls import reverse
    from django.test import Client
    client = Client()
    close_url = reverse('lostfound:lost_close', kwargs={'pk': lost.pk})
    
    # 1. Unauthenticated user post fails
    response = client.post(close_url)
    assert response.status_code == 302 # Redirect to login
    lost.refresh_from_db()
    assert lost.status == 'open'
    
    # 2. Non-authorized user post gets 403 Forbidden
    client.force_login(other_user)
    response = client.post(close_url)
    assert response.status_code == 403
    lost.refresh_from_db()
    assert lost.status == 'open'
    
    # 3. Reporter can close
    client.force_login(reporter)
    response = client.post(close_url)
    assert response.status_code == 302 # Redirect to detail
    lost.refresh_from_db()
    assert lost.status == 'closed'
    
    # Reset status back to open
    lost.status = 'open'
    lost.save()
    
    # 4. Staff can close
    client.force_login(staff)
    response = client.post(close_url)
    assert response.status_code == 302
    lost.refresh_from_db()
    assert lost.status == 'closed'
