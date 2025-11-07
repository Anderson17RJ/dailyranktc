import { useState } from "react"
import axios from 'axios'

function App() {
  const [ranking, setRanking] = useState([])
  const [loading, setLoading] = useState(false)

  const carregar = async () => {
    setLoading(true)
    const res = await axios.get('http://127.0.0.1:8000/api/top50')
    setRanking(res.data)
    setLoading(false)
  }

  return (
    <div style={{ background: "#121212", color: "white", textAlign: "center", minHeight: "100vh", padding: 20 }}>
      <h1>Ranking TheCrims</h1>
      <button onClick={carregar}>Atualizar Ranking</button>
      {loading && <p>Carregando...</p>}
      <table style={{ margin: "20px auto", borderCollapse: "collapse", width: "80%" }}>
        <thead><tr><th>Posição</th><th>Usuário</th><th>Kills Hoje</th></tr></thead>
        <tbody>
          {ranking.map((p, i) => (
            <tr key={i}>
              <td>{i + 1}</td>
              <td>{p.username}</td>
              <td>{p.kills_hoje}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;
