//*====> Action Types <====
const ADD_CONTENT = 'audio/addContent';
const FETCH_CONTENT = 'audio/fetchContent';
const FETCH_CONTENT_BY_ID = 'audio/fetchContentById';
const FETCH_CONTENT_REQUEST = 'FETCH_CONTENT_REQUEST';
const FETCH_CONTENT_SUCCESS = 'FETCH_CONTENT_SUCCESS';
const FETCH_CONTENT_FAILURE = 'FETCH_CONTENT_FAILURE';

//*====> Action Creators <====

const addContentAction = (content) => ({
  type: ADD_CONTENT,
  payload: content,
});

const fetchContentAction = (contents) => ({
  type: FETCH_CONTENT,
  payload: contents,
});

const fetchContentRequest = () => ({
  type: FETCH_CONTENT_REQUEST,
});

const fetchContentSuccess = (content) => ({
  type: FETCH_CONTENT_SUCCESS,
  payload: content,
});

const fetchContentFailure = (error) => ({
  type: FETCH_CONTENT_FAILURE,
  payload: error,
});

//*====> Thunks <====

// Add a new content

export const addNewContent = (formData) => async (dispatch) => {
  const response = await fetch('/api/audio', { // <--- line 40
    method: 'POST',
    body: formData,
  });

  console.log('Response:', response);

  if (response.ok) {
    const data = await response.json();
    dispatch(addContentAction(data));
    return data.id;
  } else {
    const error = await response.json();
    dispatch(fetchContentFailure(error.message || 'Failed to upload content'));
    console.error('Failed to upload content:', error);
  }
};

// Fetch all contents

export const fetchAudio = () => async (dispatch) => {
  const response = await fetch('/api/audio');
  if (response.ok) {
    const data = await response.json();
    dispatch(fetchContentAction(data));
  }
};

// Fetch all contents by a specific user

export const fetchContentById = (contentId) => async (dispatch) => {
  dispatch(fetchContentRequest());
  try {
    const response = await fetch(`/api/audio/${contentId}`);
    if (response.ok) {
      const data = await response.json();
      dispatch(fetchContentSuccess(data));
    } else {
      throw new Error('Failed to fetch content');
    }
  } catch (error) {
    dispatch(fetchContentFailure(error.toString()));
  }
};

//*====> Reducers <====
const initialState = {
  loading: false,
  currentContent: null,
  error: '',
  contents: [],
};

const audioReducer = (state = initialState, action) => {
  switch (action.type) {
    case FETCH_CONTENT_REQUEST:
      return {
        ...state,
        loading: true,
        error: '',
      };
    case FETCH_CONTENT_SUCCESS:
      return {
        ...state,
        loading: false,
        currentContent: action.payload,
        error: '',
      };
    case FETCH_CONTENT_FAILURE:
      return {
        ...state,
        loading: false,
        error: action.payload,
        currentContent: null,
      };
    case ADD_CONTENT:
      return { ...state, contents: [...state.contents, action.payload] };
    case FETCH_CONTENT:
      return { ...state, contents: action.payload };
    case FETCH_CONTENT_BY_ID:
      return { ...state, currentContent: action.payload };
    default:
      return state;
  }
};

export default audioReducer;
