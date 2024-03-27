import React from "react";

const MangaList = ({ mangas }) => {
    return (
        <div>
            <h2>Mangas</h2>
            <table>
                <thead>
                    <tr>
                        <th>Image</th>
                        <th>Title</th>
                        <th>Rating</th>
                        <th>Latest Chapter</th>
                        <th>Current Chapter</th>
                        <th>Chapter Diff</th>
                        <th>Link</th>
                        <th>Website</th>
                    </tr>
                </thead>
                <tbody>
                    {mangas.map((manga) => (
                        <tr key={manga.id}>
                            <td><img src={manga.imageURL} /></td>
                            <td>{manga.title}</td>
                            <td>{manga.rating}</td>
                            <td>{manga.latestChapter}</td>
                            <td>{manga.currentChapter}</td>
                            <td>{manga.chapterDiff}</td>
                            <td><a href={manga.link}>link</a></td>
                            <td>{manga.website}</td>
                            <td>
                                <button>Update</button>
                                <button>Delete</button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

export default MangaList;