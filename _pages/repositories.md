---
layout: page
permalink: /repositories/
title: Repositories
description: Selected GitHub repositories.
nav: true
nav_order: 4
---

{% assign cards = site.data.repo_cards %}
{% assign description_lines = site.data.repositories.repo_description_lines_max | default: 2 %}

<style>
  .repo-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(min(100%, 20rem), 1fr));
    gap: 1rem;
    margin-bottom: 1.5rem;
  }

  .repo-card {
    position: relative;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    padding: 1rem;
    border: 1px solid var(--global-divider-color);
    border-radius: 0.5rem;
    background-color: var(--global-card-bg-color);
    transition:
      border-color 0.2s ease,
      transform 0.2s ease;
  }

  .repo-card:hover {
    border-color: var(--global-theme-color);
    transform: translateY(-2px);
  }

  .repo-card__head {
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }

  .repo-card__icon {
    color: var(--global-text-color-light);
  }

  .repo-card__title {
    font-weight: 600;
    overflow-wrap: anywhere;
  }

  /* Makes the whole card clickable while keeping the homepage link separately focusable. */
  .repo-card__title::after {
    content: "";
    position: absolute;
    inset: 0;
  }

  .repo-card__badge {
    padding: 0 0.5rem;
    border: 1px solid var(--global-divider-color);
    border-radius: 999px;
    font-size: 0.75rem;
    color: var(--global-text-color-light);
  }

  .repo-card__description {
    display: -webkit-box;
    -webkit-box-orient: vertical;
    -webkit-line-clamp: {{ description_lines }};
    line-clamp: {{ description_lines }};
    overflow: hidden;
    min-height: calc({{ description_lines }} * 1.5em);
    margin: 0;
    font-size: 0.9rem;
    color: var(--global-text-color-light);
  }

  .repo-card__meta {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 0.75rem;
    margin-top: auto;
    font-size: 0.8rem;
    color: var(--global-text-color-light);
  }

  .repo-card__language {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
  }

  .repo-card__dot {
    width: 0.7rem;
    height: 0.7rem;
    border-radius: 50%;
    display: inline-block;
  }

  .repo-card__home {
    position: relative;
    z-index: 1;
    margin-left: auto;
  }

  .repo-profile {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 1rem;
    padding: 1rem;
    margin-bottom: 1.5rem;
    border: 1px solid var(--global-divider-color);
    border-radius: 0.5rem;
    background-color: var(--global-card-bg-color);
  }

  .repo-profile__avatar {
    width: 4rem;
    height: 4rem;
    border-radius: 50%;
  }

  .repo-profile__meta {
    display: flex;
    flex-wrap: wrap;
    gap: 0.75rem;
    font-size: 0.85rem;
    color: var(--global-text-color-light);
  }

  .repo-updated {
    font-size: 0.8rem;
    color: var(--global-text-color-light);
  }
</style>

{% if cards.users and cards.users.size > 0 %}

## GitHub users

{% for user in cards.users %}

  <div class="repo-profile">
    <img class="repo-profile__avatar" src="{{ user.avatar_url }}" alt="{{ user.login }}" loading="lazy">
    <div>
      <div><a href="{{ user.html_url }}" rel="external nofollow noopener" target="_blank">{{ user.name }}</a></div>
      {% if user.bio %}<div class="repo-profile__meta">{{ user.bio }}</div>{% endif %}
      <div class="repo-profile__meta">
        <span><i class="fa-solid fa-book-bookmark"></i> {{ user.public_repos }} repositories</span>
        <span><i class="fa-solid fa-user-group"></i> {{ user.followers }} followers</span>
        {% if user.location %}<span><i class="fa-solid fa-location-dot"></i> {{ user.location }}</span>{% endif %}
      </div>
    </div>
  </div>
  {% endfor %}
  {% endif %}

{% if cards.repos and cards.repos.size > 0 %}

## GitHub Repositories

  <div class="repo-grid">
    {% for repo in cards.repos %}
      <div class="repo-card">
        <div class="repo-card__head">
          <i class="fa-solid fa-book repo-card__icon"></i>
          <a class="repo-card__title" href="{{ repo.html_url }}" rel="external nofollow noopener" target="_blank">{{ repo.name }}</a>
          {% if repo.archived %}<span class="repo-card__badge">Archived</span>{% endif %}
        </div>
        <p class="repo-card__description">{{ repo.description }}</p>
        <div class="repo-card__meta">
          {% if repo.language %}
            <span class="repo-card__language">
              <span class="repo-card__dot" style="background-color: {{ repo.language_color }}"></span>{{ repo.language }}
            </span>
          {% endif %}
          <span><i class="fa-regular fa-star"></i> {{ repo.stars }}</span>
          <span><i class="fa-solid fa-code-fork"></i> {{ repo.forks }}</span>
          {% if repo.homepage %}
            <a class="repo-card__home" href="{{ repo.homepage }}" rel="external nofollow noopener" target="_blank">
              <i class="fa-solid fa-arrow-up-right-from-square"></i> Demo
            </a>
          {% endif %}
        </div>
      </div>
    {% endfor %}
  </div>
{% endif %}

{% if cards.metadata.last_updated %}

<p class="repo-updated">Repository stats last refreshed on {{ cards.metadata.last_updated }}.</p>
{% endif %}
