import { useEffect, useState } from "react";

export default function usePolling(fetcher, interval = 10000) {
  const [data, setData] = useState(null);

  useEffect(() => {
    let active = true;

    const load = async () => {
      const res = await fetcher();
      if (active) setData(res.data);
    };

    load();
    const id = setInterval(load, interval);

    return () => {
      active = false;
      clearInterval(id);
    };
  }, []);

  return data;
}
