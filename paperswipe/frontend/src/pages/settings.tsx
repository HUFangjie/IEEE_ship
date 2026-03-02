import { useEffect, useState } from 'react';
import { apiGet, apiPost } from '../lib/api';

export default function Settings() {
  const [form, setForm] = useState<any>({llm_provider:'openai', library_path:'./library'});
  useEffect(()=>{apiGet('/api/settings').then((s)=>setForm((f:any)=>({...f,...s})));},[]);
  return <main style={{padding:20}}>
    <h2>Settings</h2>
    <input placeholder="IEEE API key" onChange={(e)=>setForm({...form,ieee_api_key:e.target.value})}/>
    <select value={form.llm_provider} onChange={(e)=>setForm({...form,llm_provider:e.target.value})}><option value="openai">openai</option><option value="gemini">gemini</option></select>
    <input placeholder="OpenAI API key" onChange={(e)=>setForm({...form,openai_api_key:e.target.value})}/>
    <input value={form.library_path} onChange={(e)=>setForm({...form,library_path:e.target.value})}/>
    <button onClick={async()=>{await apiPost('/api/settings',form); alert('Saved');}}>Save</button>
    <button onClick={async()=>{await apiPost('/api/search',{publication:'TIFS',query:'test',year_from:2024,year_to:2026,limit:1}); alert('IEEE test triggered')}}>Test IEEE</button>
    <button onClick={async()=>{await apiPost('/api/search',{publication:'TIFS',query:'abstract security',year_from:2024,year_to:2026,limit:1}); alert('LLM test via fetch')}}>Test LLM</button>
  </main>
}
