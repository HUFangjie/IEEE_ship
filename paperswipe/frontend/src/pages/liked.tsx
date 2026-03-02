import { useEffect, useState } from 'react';
import { apiGet, apiPost } from '../lib/api';

export default function Liked() {
  const [tag, setTag] = useState('');
  const [items, setItems] = useState<any[]>([]);
  const [exported, setExported] = useState('');
  useEffect(()=>{apiGet('/api/liked?publication=TIFS').then(setItems);},[]);

  return <main style={{padding:20}}>
    <h2>Liked</h2>
    <input placeholder="tag filter" value={tag} onChange={(e)=>setTag(e.target.value)} />
    <button onClick={async()=>setItems(await apiGet(`/api/liked?publication=TIFS&tag=${encodeURIComponent(tag)}`))}>Filter</button>
    <button onClick={async()=>setExported((await apiPost('/api/export/bib',{})).content)}>Export Bib</button>
    <button onClick={async()=>setExported((await apiPost('/api/export/csv',{})).content)}>Export CSV</button>
    <pre style={{whiteSpace:'pre-wrap'}}>{exported}</pre>
    <ul>{items.map((x)=><li key={x.paper_id}>{x.title} ({x.year}) [{x.tags}] <a href={x.url} target="_blank">Open</a></li>)}</ul>
  </main>
}
