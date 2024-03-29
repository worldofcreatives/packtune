import { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { fetchUserProfile } from '../../redux/profile';
import './ProfilePage.css'; // Adjust the path as necessary
import { useNavigate } from 'react-router-dom';

const ProfilePage = () => {
  const dispatch = useDispatch();
  const userProfile = useSelector((state) => state.profile.userProfile);
  const navigate = useNavigate();

  useEffect(() => {
    dispatch(fetchUserProfile());
  }, [dispatch]);

  if (!userProfile) {
    return <div>Loading...</div>;
  }

  const { creator, company } = userProfile;

  return (
    <div className="profile-page">
      <h1>Profile Information</h1>
      <button onClick={() => navigate('/profile/edit')}>Edit Profile</button>
      {userProfile.type === 'Creator' && creator && (
        <div>
          <h2>Creator Profile</h2>
          {creator.profile_pic && <img src={creator.profile_pic} alt="Profile" className='profile-pic'/>}
          <p><strong>Stage Name:</strong> {creator.stage_name}</p>
          <p><strong>Bio:</strong> {creator.bio}</p>
          <p><strong>First Name:</strong> {creator.first_name}</p>
          <p><strong>Last Name:</strong> {creator.last_name}</p>
          <p><strong>Phone:</strong> {creator.phone}</p>
          <p><strong>Address:</strong> {`${creator.address_1} ${creator.address_2 || ''}, ${creator.city}, ${creator.state} ${creator.postal_code}`}</p>
          <p><strong>Portfolio URL:</strong> <a href={creator.portfolio_url}>{creator.portfolio_url}</a></p>
          <p><strong>Previous Projects:</strong> {creator.previous_projects}</p>
          <p><strong>Instagram:</strong> <a href={`https://instagram.com/${creator.instagram}`}>{creator.instagram}</a></p>
          <p><strong>Twitter:</strong> <a href={`https://twitter.com/${creator.twitter}`}>{creator.twitter}</a></p>
          <p><strong>Facebook:</strong> <a href={creator.facebook}>{creator.facebook}</a></p>
          <p><strong>YouTube:</strong> <a href={creator.youtube}>{creator.youtube}</a></p>
          <p><strong>Other Social Media:</strong> {creator.other_social_media}</p>
          <p><strong>Reference Name:</strong> {creator.reference_name}</p>
          <p><strong>Reference Email:</strong> {creator.reference_email}</p>
          <p><strong>Reference Phone:</strong> {creator.reference_phone}</p>
          <p><strong>Reference Relationship:</strong> {creator.reference_relationship}</p>
        </div>
      )}
      {userProfile.type === 'Company' && company && (
        <div>
          <h2>Company Profile</h2>
          <p><strong>Name:</strong> {company.name}</p>
          <p><strong>Bio:</strong> {company.bio}</p>
          {company.logo && <img src={company.logo} alt="Logo" />}
          {/* Display other company-specific information here */}
        </div>
      )}
    </div>
  );
};

export default ProfilePage;
