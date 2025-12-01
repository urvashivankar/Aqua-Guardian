-- Add Dashboard Tables for Aqua Guardian
-- Run this in the Supabase SQL Editor

-- Water Quality Readings Table
CREATE TABLE IF NOT EXISTS public.water_quality_readings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    location TEXT DEFAULT 'Default Monitoring Station',
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    ph NUMERIC(4,2) NOT NULL,
    turbidity NUMERIC(5,2) NOT NULL,
    oxygen NUMERIC(5,2) NOT NULL,
    salinity NUMERIC(5,2) NOT NULL,
    temperature NUMERIC(5,2) NOT NULL,
    recorded_at TIMESTAMPTZ DEFAULT timezone('utc', now())
);

-- Success Stories Table
CREATE TABLE IF NOT EXISTS public.success_stories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title TEXT NOT NULL,
    location TEXT NOT NULL,
    timeframe TEXT NOT NULL,
    description TEXT NOT NULL,
    image_url TEXT,
    status TEXT DEFAULT 'Ongoing Success',
    water_quality_improved INTEGER,
    species_recovered INTEGER,
    lives_impacted INTEGER,
    pollution_reduced INTEGER,
    challenges JSONB DEFAULT '[]'::jsonb,
    solutions JSONB DEFAULT '[]'::jsonb,
    results JSONB DEFAULT '[]'::jsonb,
    stakeholders JSONB DEFAULT '[]'::jsonb,
    created_at TIMESTAMPTZ DEFAULT timezone('utc', now()),
    updated_at TIMESTAMPTZ DEFAULT timezone('utc', now())
);

-- Enable RLS
ALTER TABLE public.water_quality_readings ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.success_stories ENABLE ROW LEVEL SECURITY;

-- RLS Policies for Water Quality Readings
CREATE POLICY "allow public read water quality"
    ON public.water_quality_readings
    FOR SELECT
    TO authenticated, anon
    USING (true);

CREATE POLICY "allow authenticated insert water quality"
    ON public.water_quality_readings
    FOR INSERT
    TO authenticated
    WITH CHECK (true);

-- RLS Policies for Success Stories
CREATE POLICY "allow public read success stories"
    ON public.success_stories
    FOR SELECT
    TO authenticated, anon
    USING (true);

CREATE POLICY "allow authenticated insert success stories"
    ON public.success_stories
    FOR INSERT
    TO authenticated
    WITH CHECK (true);

-- Seed Data: Success Stories
INSERT INTO public.success_stories (
    title, location, timeframe, description, image_url, status,
    water_quality_improved, species_recovered, lives_impacted, pollution_reduced,
    challenges, solutions, results, stakeholders
) VALUES 
(
    'Chilika Lake Restoration',
    'Odisha, India',
    '2022-2024',
    'Through community collaboration and scientific intervention, Chilika Lake has seen remarkable recovery in biodiversity and water quality.',
    '/assets/success_story_chilika.png',
    'Ongoing Success',
    85, 23, 15000, 67,
    '["Industrial pollution from nearby factories", "Unregulated fishing practices", "Sedimentation from agricultural runoff"]'::jsonb,
    '["Implementation of strict pollution controls", "Community-based sustainable fishing programs", "Wetland restoration and buffer zones"]'::jsonb,
    '["Return of endangered Irrawaddy dolphins", "85% improvement in water clarity", "Restoration of 200+ bird species habitat"]'::jsonb,
    '["Local Communities", "Environmental NGOs", "Government", "Research Institutions"]'::jsonb
),
(
    'Mumbai Harbor Clean-up Initiative',
    'Mumbai, Maharashtra',
    '2023-2024',
    'Massive citizen-led cleanup effort transformed Mumbai Harbor from a pollution hotspot to a recovering marine ecosystem.',
    '/assets/success_story_mumbai.png',
    'Significant Progress',
    72, 15, 25000, 58,
    '["Heavy industrial discharge", "Plastic waste accumulation", "Oil spills from shipping activities"]'::jsonb,
    '["Daily waste collection drives", "Industrial compliance monitoring", "Community awareness campaigns"]'::jsonb,
    '["Removed 500 tons of plastic waste", "Installed 50 water quality sensors", "Trained 1000+ volunteer guardians"]'::jsonb,
    '["Citizens", "Mumbai Port Trust", "Environmental Groups", "Local Government"]'::jsonb
),
(
    'Kerala Backwaters Revival',
    'Kerala, India',
    '2021-2024',
    'Comprehensive ecosystem restoration bringing back the pristine beauty and biodiversity of Kerala backwaters.',
    '/assets/success_story_kerala.png',
    'Model Success',
    91, 34, 12000, 78,
    '["Tourism-related pollution", "Uncontrolled boat traffic", "Sewage discharge from houseboats"]'::jsonb,
    '["Eco-friendly tourism guidelines", "Sustainable transportation systems", "Advanced waste treatment facilities"]'::jsonb,
    '["Zero plastic policy implementation", "Return of native fish species", "Sustainable tourism model adopted"]'::jsonb,
    '["Tourism Industry", "Local Fishermen", "State Government", "Conservation Groups"]'::jsonb
);

-- Seed Data: Initial Water Quality Reading
INSERT INTO public.water_quality_readings (
    location, latitude, longitude, ph, turbidity, oxygen, salinity, temperature
) VALUES 
(
    'Mumbai Harbor Monitoring Station',
    19.0760, 72.8777,
    7.2, 2.1, 8.5, 0.5, 24.0
);
