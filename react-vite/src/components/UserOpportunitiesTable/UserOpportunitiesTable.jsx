import { useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { Link } from 'react-router-dom';
import { fetchUserOpportunities } from '../../redux/useropps';

const UserOpportunitiesTable = () => {
  const dispatch = useDispatch();
  const { opportunities } = useSelector(state => ({
    opportunities: state.useropps.opportunities.created_opportunities,
  }));

  useEffect(() => {
    dispatch(fetchUserOpportunities());
  }, [dispatch]);

  return (
    <table>
      <thead>
        <tr>
          <th>Opportunity Name</th>
          <th>Date Added</th>
          <th>Date Updated</th>
          <th># of Submissions</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        {opportunities.map((opportunity) => (
          <tr key={opportunity.id}>
            <td>{opportunity.name}</td>
            <td>{new Date(opportunity.created_date).toLocaleDateString()}</td>
            <td>{new Date(opportunity.updated_date).toLocaleDateString()}</td>
            <td>{/* Calculate # of submissions for this opportunity */}</td>
            <td>
              <Link to={`/opps/${opportunity.id}/subs`}>View Submissions</Link>
              {' | '}
              <Link to={`/opps/${opportunity.id}`}>View Opportunity</Link>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default UserOpportunitiesTable;
