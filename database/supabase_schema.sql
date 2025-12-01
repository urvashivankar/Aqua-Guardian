-- Aqua Guardian Supabase Schema
-- Run this migration inside your Supabase SQL editor

create table if not exists public.users (
    id uuid primary key default gen_random_uuid(),
    email text unique not null,
    full_name text,
    role text default 'citizen',
    avatar_url text,
    metadata jsonb default '{}'::jsonb,
    inserted_at timestamptz default timezone('utc', now())
);

create table if not exists public.reports (
    id uuid primary key default gen_random_uuid(),
    user_id uuid references public.users(id) on delete set null,
    latitude double precision not null,
    longitude double precision not null,
    description text not null,
    severity integer not null check (severity between 1 and 10),
    ai_class text,
    ai_confidence numeric(5,2),
    status text default 'pending',
    blockchain_tx text,
    created_at timestamptz default timezone('utc', now())
);

create table if not exists public.photos (
    id uuid primary key default gen_random_uuid(),
    report_id uuid references public.reports(id) on delete cascade,
    url text not null,
    metadata jsonb default '{}'::jsonb,
    created_at timestamptz default timezone('utc', now())
);

create table if not exists public.cleanup_actions (
    id uuid primary key default gen_random_uuid(),
    report_id uuid references public.reports(id) on delete cascade,
    actor_id uuid references public.users(id) on delete set null,
    status text default 'in_progress',
    notes text,
    evidence_urls text[] default '{}',
    started_at timestamptz default timezone('utc', now()),
    completed_at timestamptz
);

create table if not exists public.blockchain_logs (
    id uuid primary key default gen_random_uuid(),
    report_id uuid references public.reports(id) on delete cascade,
    tx_hash text not null,
    network text default 'testnet',
    inserted_at timestamptz default timezone('utc', now())
);

create table if not exists public.rewards (
    id uuid primary key default gen_random_uuid(),
    user_id uuid references public.users(id) on delete cascade,
    points integer default 0,
    tier text default 'blue',
    metadata jsonb default '{}'::jsonb,
    updated_at timestamptz default timezone('utc', now())
);

alter table public.reports enable row level security;
alter table public.photos enable row level security;
alter table public.cleanup_actions enable row level security;
alter table public.blockchain_logs enable row level security;
alter table public.rewards enable row level security;

create policy "allow authenticated read reports"
    on public.reports
    for select
    to authenticated, anon
    using (true);

create policy "allow authenticated insert reports"
    on public.reports
    for insert
    to authenticated
    with check (auth.uid() = user_id);

create policy "allow maintainers update cleanup"
    on public.cleanup_actions
    for update
    to authenticated
    using (true);


