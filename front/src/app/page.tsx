
type Data ={
  message:string
}
export default async function Home() {
  const API_URL = process.env.API_BASE_URL
  console.log(API_URL);
  

  const devURL = "http://127.0.0.1:9003/api/"
  const res = await fetch(`${API_URL}`)
  const data = await res.json() 
  console.log(data.message);
 

  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
    Dark Search Main Page <br></br>
    API Response: {data.message}
    </main>
  );
}
