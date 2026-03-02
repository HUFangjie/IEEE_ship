import { useState } from 'react';
import { useRouter } from 'next/router';
import { apiPost } from '../lib/api';

export default function Home() {
  const router = useRouter();
  const [query, setQuery] = useState('federated learning');
  const [yearFrom, setYearFrom] = useState(2022);
  const [yearTo, setYearTo] = useState(new Date().getFullYear());
  const [limit, setLimit] = useState(50);

  return <main style={{padding:20}}>
    <h1>PaperSwipe</h1>
    <p><a href="/settings">Settings</a> | <a href="/liked">Liked</a></p>
    <input value={query} onChange={(e)=>setQuery(e.target.value)} />
    <input type="number" value={yearFrom} onChange={(e)=>setYearFrom(parseInt(e.target.value))} />
    <input type="number" value={yearTo} onChange={(e)=>setYearTo(parseInt(e.target.value))} />
    <select value={limit} onChange={(e)=>setLimit(parseInt(e.target.value))}><option>20</option><option>50</option><option>100</option></select>
    <button onClick={async ()=>{
      const r = await apiPost('/api/search', { publication: 'TIFS', query, year_from: yearFrom, year_to: yearTo, limit });
      router.push(`/swipe?job=${r.job_id}&query=${encodeURIComponent(query)}`);
    }}>Fetch & Start</button>
  </main>
}
