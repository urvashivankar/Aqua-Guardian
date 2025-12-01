-- Run this in the Supabase SQL Editor to fix the missing columns in the reports table

ALTER TABLE public.reports ADD COLUMN IF NOT EXISTS severity integer CHECK (severity between 1 and 10);
ALTER TABLE public.reports ADD COLUMN IF NOT EXISTS ai_class text;
ALTER TABLE public.reports ADD COLUMN IF NOT EXISTS ai_confidence numeric(5,2);
ALTER TABLE public.reports ADD COLUMN IF NOT EXISTS status text default 'pending';
ALTER TABLE public.reports ADD COLUMN IF NOT EXISTS blockchain_tx text;
ALTER TABLE public.reports ADD COLUMN IF NOT EXISTS created_at timestamptz default timezone('utc', now());
