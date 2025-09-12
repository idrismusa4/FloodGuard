-- FloodGuardian AI - Supabase Schema
-- Run this in Supabase → SQL editor

-- Users table
create table if not exists public.users (
    id bigserial primary key,
    name text not null,
    phone text not null unique,
    location text not null,
    created_at timestamp with time zone default now()
);

-- Predictions table
create table if not exists public.predictions (
    id bigserial primary key,
    region text not null,
    severity double precision not null,
    prediction_data jsonb,
    created_at timestamp with time zone default now()
);

-- Alerts table
create table if not exists public.alerts (
    id bigserial primary key,
    user_id bigint references public.users(id) on delete cascade,
    message text not null,
    sent_at timestamp with time zone default now()
);

-- Resources table
create table if not exists public.resources (
    id bigserial primary key,
    region text not null,
    resource_type text not null,
    quantity integer not null,
    details jsonb,
    allocated_at timestamp with time zone default now()
);

-- Helpful indexes
create index if not exists idx_predictions_region_created_at on public.predictions(region, created_at desc);
create index if not exists idx_alerts_user_id_sent_at on public.alerts(user_id, sent_at desc);
create index if not exists idx_resources_region on public.resources(region);

-- RLS (optional for service role usage; keep disabled or add policies)
-- alter table public.users enable row level security;
-- alter table public.predictions enable row level security;
-- alter table public.alerts enable row level security;
-- alter table public.resources enable row level security;

