/* eslint-disable react/jsx-filename-extension, jsx-a11y/media-has-caption */
import React, { useState, useRef } from 'react';
import './App.css';

/**
 *
 */
function App() {
  // fetches JSON data passed in by flask.render_template and loaded
  // in public/index.html in the script with id "data"
  const args = JSON.parse(document.getElementById('data').text);
  const [newArtist, setNewArtist] = useState([]);
  const textInput = useRef(null);
  const [message, setMessage] = useState('');

  function addArtist() {
    const newItem = textInput.current.value;
    const newListArtist = [...newArtist, newItem];
    setNewArtist(newListArtist);
    textInput.current.value = '';
  }

  function deleteArtist(artistId) {
    const newListArtist = newArtist.filter((item) => item !== artistId);
    setNewArtist(newListArtist);
  }

  function submitArtistAdded() {
    fetch('/save', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ new_artist: newArtist }),
    }).then((response) => response.json()).then((data) => {
      setMessage(data.reason);
      setNewArtist([]);
    });
  }

  return (
    <>
      <div>
        <h1>
          {args.username}
        </h1>
        <form action="/signout" method="POST">
          <button className="signOut" type="submit">Sign out</button>
        </form>
      </div>

      <h1>Add a favorite artist ID:</h1>
      <p>{message}</p>
      <div>
        <input ref={textInput} type="text" />
        <button className="addArtist" onClick={addArtist} type="submit">Add Artist</button>
        <ul>
          {newArtist.map((artistId) => (
            <li>
              {artistId}
              {' '}
              <button className="deleteArtist" onClick={() => deleteArtist(artistId)} type="submit">x</button>
            </li>
          ))}
        </ul>
        <button onClick={submitArtistAdded} type="submit">Save</button>
      </div>

      {args.has_artists_saved ? (
        <>
          <h2>{args.song_name}</h2>
          <h3>{args.song_artist}</h3>
          <div>
            <img src={args.song_image_url} width={300} height={300} alt="song" />
          </div>
          <div>
            <audio controls>
              <source src={args.preview_url} />
            </audio>
          </div>
          <a href={args.genius_url}> Click here to see lyrics! </a>
        </>
      )
        : (<h2>Looks like you do not have anything saved! Use the form below!</h2>)}
    </>
  );
  // TODO: Implement your main page as a React component.
}

export default App;
