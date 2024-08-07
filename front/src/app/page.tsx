

export default async function Home() {
  const API_URL = process.env.API_BASE_URL
  console.log(API_URL);
  
let data
 try {
   const res = await fetch(`${API_URL}`)
  data = await res.json() 
  console.log(data);
  return data
 } catch (error) {
  console.log(error);
  
 }

 const {message} = data
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
    Dark Search Main Page
    API: {message}
    </main>
  );
}
