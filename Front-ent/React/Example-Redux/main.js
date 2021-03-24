console.log(window.Redux)

const { createStore } = window.Redux;

const initialState = [
  'Listen to music'
];

const hobbyReducer = ( state = initialState, action ) => {
  return state;
}

const store = createStore(hobbyReducer);

// RENDER REDUX HOBBY LIST
const renderHobbyList = (hobbyList) => {
  if ( !Array.isArray(hobbyList) || hobbyList.length === 0) return;

  const ulElement = document.querySelector('#hobbyListId');
  if (!ulElement) return;

  ulElement.innerHTML = '';
}