import { NextRequest } from "next/server";


type RouteContext = {
  params: Promise<{ path: string[] }>;
};


async function proxy(request: NextRequest, context: RouteContext) {
  const backendUrl = process.env.BACKEND_URL;

  if (!backendUrl) {
    return Response.json({ error: "Brak konfiguracji BACKEND_URL." }, { status: 500 });
  }

  const { path } = await context.params;
  const target = new URL(`/api/${path.join("/")}`, backendUrl);
  target.search = request.nextUrl.search;

  const headers = new Headers(request.headers);
  headers.delete("host");
  headers.delete("content-length");
  if (headers.has("origin")) {
    headers.set("origin", target.origin);
  }

  const response = await fetch(target, {
    method: request.method,
    headers,
    body: ["GET", "HEAD"].includes(request.method)
      ? undefined
      : await request.arrayBuffer(),
    redirect: "manual",
  });

  return new Response(response.body, {
    status: response.status,
    headers: response.headers,
  });
}


export const dynamic = "force-dynamic";
export const GET = proxy;
export const POST = proxy;
