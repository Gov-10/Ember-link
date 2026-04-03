"use client";
import { useRouter } from "next/navigation";
import {fetchAuthSession, signOut} from "aws-amplify/auth";
export default function Hello(){
  const router = useRouter();
  const handle = async()=>{
    const abc = localStorage.getItem("cognito_token");
console.log(abc);
  }
  const handleLogout = async () => {
    await signOut();
    router.push("/login");
  };
  return (<div>Hello
           <button onClick={handle}>HOLA</button>
           <button onClick={handleLogout}>BYE</button>
          </div>);
}
