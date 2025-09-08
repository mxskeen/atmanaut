import { BarLoader } from "react-spinners";

export default function Loading() {
  // You can add any UI inside Loading, including a Skeleton.
  return (
    <BarLoader
      color="#ffe066"
      width={"100%"}
      speedMultiplier={1.2}
      height={6}
      className="mb-4 shadow-glow"
      style={{
        borderRadius: 8,
        boxShadow: "0 0 16px #ffe06688",
        transition: "all 0.5s cubic-bezier(0.4,0,0.2,1)",
      }}
    />
  );
}
