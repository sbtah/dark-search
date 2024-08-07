

export default async function Home() {
  const API_URL = process.env.API_BASE_URL
  console.log(API_URL);
  

 try {
   const res = await fetch(`${API_URL}`)
   const data = await res.json() 
  console.log(data);
 } catch (error) {
  console.log(error);
  
 }

 
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
Dark Search Main Page d
    </main>
  );
}
