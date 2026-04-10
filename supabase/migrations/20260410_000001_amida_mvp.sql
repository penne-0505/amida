create extension if not exists pgcrypto;

create or replace function public.set_updated_at()
returns trigger
language plpgsql
as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

create table if not exists public.guild_templates (
  template_id uuid primary key default gen_random_uuid(),
  guild_id text not null,
  title text not null,
  title_normalized text generated always as (
    lower(regexp_replace(btrim(title), '\s+', ' ', 'g'))
  ) stored,
  options jsonb not null,
  created_by text not null,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  constraint guild_templates_title_not_blank check (length(btrim(title)) > 0),
  constraint guild_templates_options_non_empty check (
    jsonb_typeof(options) = 'array'
    and jsonb_array_length(options) > 0
  ),
  constraint guild_templates_unique_guild_title unique (guild_id, title_normalized),
  constraint guild_templates_template_id_guild_id_unique unique (template_id, guild_id)
);

create trigger trg_guild_templates_updated_at
before update on public.guild_templates
for each row execute function public.set_updated_at();

create table if not exists public.user_guild_last_used_templates (
  user_id text not null,
  guild_id text not null,
  source_template_id uuid null,
  template_snapshot jsonb not null,
  updated_at timestamptz not null default now(),
  constraint user_guild_last_used_templates_pkey primary key (user_id, guild_id),
  constraint user_guild_last_used_templates_snapshot_object check (
    jsonb_typeof(template_snapshot) = 'object'
    and template_snapshot ? 'title'
    and length(btrim(template_snapshot ->> 'title')) > 0
    and template_snapshot ? 'options'
    and jsonb_typeof(template_snapshot -> 'options') = 'array'
    and jsonb_array_length(template_snapshot -> 'options') > 0
  ),
  constraint user_guild_last_used_templates_source_template_fk
    foreign key (source_template_id, guild_id)
    references public.guild_templates (template_id, guild_id)
    on delete set null
);

create trigger trg_user_guild_last_used_templates_updated_at
before update on public.user_guild_last_used_templates
for each row execute function public.set_updated_at();
