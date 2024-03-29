import React, { useEffect, useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { useNavigate, useParams } from 'react-router-dom';
import { fetchSubmissionsForOpportunity } from '../../redux/submissions';
import SubmissionItem from '../SubmissionItem';
import MusicPlayer from '../MusicPlayer/MusicPlayer';
import './Submissions.css';

const Submissions = () => {
  const { oppId } = useParams();
  const dispatch = useDispatch();
  const { user } = useSelector((state) => state.session);
  const { submissions, loading, error } = useSelector((state) => state.submissions);
  const isCompany = user && user.type === 'Company';
  const [currentSong, setCurrentSong] = useState({ url: '', name: '' });
  const [playing, setPlaying] = useState(false);
  const navigate = useNavigate();

  const playSong = (songUrl, songName) => {
    if (currentSong.url !== songUrl) {
      setCurrentSong({ url: songUrl, name: songName });
    } else {
      setCurrentSong({ url: '', name: '' }); // If the same song is clicked, stop playing
    }
  };


  useEffect(() => {
    if (isCompany || user) {
      dispatch(fetchSubmissionsForOpportunity(oppId));
    }
  }, [dispatch, oppId, isCompany, user]);

  // Define the order of the sections
  const statusOrder = ['Pending', 'Reviewing', 'Accepted', 'Rejected'];

  // Organize submissions by status
  const organizedSubmissions = submissions.reduce((acc, submission) => {
    (acc[submission.status] = acc[submission.status] || []).push(submission);
    return acc;
  }, {});

  if (loading) {
    return <div>Loading submissions...</div>;
  }

  if (error) {
    // return <div>Error: {error}</div>;
    navigate('/opps');
    return <div>You are not authorized to view these submissions.</div>;
  }

  // Filter submissions if user is not a company
  const visibleSubmissions = isCompany
    ? submissions
    : submissions.filter((submission) => submission.creator_id === user.id);

  const downloadAllFiles = async (status) => {
    const submissionsToDownload = organizedSubmissions[status];
    try {
      const response = await fetch(`/api/aws/download-all/packtune`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(submissionsToDownload)
      });

      if (!response.ok) {
        throw new Error(`Failed to download files: ${response.statusText}`);
      }

      const blob = await response.blob();
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `${status}-submissions.zip`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    } catch (error) {
      console.error(`Error during bulk file download: ${error.message}`);
    }
  };

    return (
      <div>
        <div className='sub-top'>
          <h2>Submissions</h2>
          {statusOrder.map(status => (
            organizedSubmissions[status] && organizedSubmissions[status].length > 0 && (
              <div key={status} className="status-section">
                <div className='sub-top-2'>
                <h3>{status}</h3>
                <button onClick={() => downloadAllFiles(status)} className="download-all-button">Download All {status}</button>
                </div>
                <ul>
                  {organizedSubmissions[status].map(submission => (
                    <SubmissionItem key={submission.id} submission={submission} onPlay={playSong} />
                  ))}
                </ul>
              </div>
            )
          ))}
        </div>
        <div className="music-player-wrapper">
          <MusicPlayer audioUrl={currentSong.url} songName={currentSong.name} />
        </div>
      </div>
    );
  };

export default Submissions;
