# lena-var4.com — Germany Blog 구축 요청

## 프로젝트 개요
- 사이트: lena-var4.com (GitHub Pages + Jekyll)
- 이번 작업 범위: /germany/ 독일 생활 블로그 전체 구축
- 메인 index.html은 이미 완성되어 있음 — 건드리지 말 것
- 언어: 한국어 / 영어 병행

---

## 레이아웃 구조

### 2컬럼 레이아웃 (목록 페이지 + 글 상세 페이지 동일하게 적용)
- 좌측 (메인, 약 65%): 목록 페이지는 최신 글 카드, 상세 페이지는 글 본문
- 우측 (사이드바, 약 35%): 전체 글 목록 항상 표시 — sticky로 스크롤해도 고정
  - 최신순 정렬, 날짜 + 제목
  - 현재 보고 있는 글은 하이라이트
  - 태그 필터 (클릭 시 해당 태그 글만 표시)
  - 총 글 수 카운터
- 모바일: 사이드바는 본문 아래로 자연스럽게 배치

---

## 디렉토리 구조 (이대로 만들 것)

```
lena-var4.com/
├── index.html                          ← 이미 완성, 수정 금지
├── _layouts/
│   ├── default.html
│   └── germany/
│       ├── index.html                  ← 글 목록 레이아웃
│       └── post.html                   ← 글 상세 레이아웃
├── _includes/
│   ├── head.html                       ← SEO 메타태그 공통
│   ├── nav.html                        ← 사이트 공통 네비게이션
│   ├── footer.html                     ← 사이트 공통 푸터
│   └── germany/
│       ├── sidebar.html                ← 우측 글 목록 사이드바
│       ├── post-card.html              ← 글 카드 컴포넌트
│       └── seo.html                    ← Germany SEO 메타 자동 생성
├── _posts/germany/                     ← 글 파일 폴더
│   └── 2026-03-12-german-weather.md   ← 첫 번째 글 예시
├── assets/
│   ├── css/
│   │   ├── main.css                    ← 전체 공통 CSS
│   │   └── germany/
│   │       ├── layout.css              ← Germany 레이아웃 CSS
│   │       └── themes/
│   │           ├── default.css
│   │           ├── weather.css
│   │           ├── cozy.css
│   │           ├── city.css
│   │           └── food.css
│   └── images/germany/                 ← 글별 이미지 폴더
├── _data/
│   └── germany_tags.yml
├── germany/
│   └── index.html                      ← 블로그 진입점
├── _config.yml
├── sitemap.xml
└── robots.txt
```

---

## 테마 시스템 (핵심 기능)

글마다 다른 배경/분위기를 적용하는 시스템.
Lena가 front matter에 `theme: weather` 한 줄만 쓰면 자동으로 해당 CSS 로드.

### _layouts/germany/post.html 안에 이 한 줄 포함:
```html
<link rel="stylesheet" href="/assets/css/germany/themes/{{ page.theme | default: 'default' }}.css">
```

### 각 테마 CSS는 아래 CSS 변수를 오버라이드하는 방식:
```css
:root {
  --theme-bg:        #ffffff;
  --theme-hero-bg:   linear-gradient(...);
  --theme-accent:    #000000;
  --theme-text:      #000000;
  --theme-card-bg:   rgba(255,255,255,0.8);
  --theme-font-body: 'Nunito', sans-serif;
}
```

### 1차 납품 테마 5종:
- `default` — 흰 배경, 깔끔한 타이포
- `weather` — 하늘색 그라디언트, 구름/비 CSS 애니메이션
- `cozy` — 따뜻한 베이지, 소프트 그림자
- `city` — 다크 배경 + 네온 포인트 컬러
- `food` — 따뜻한 오렌지/레드 계열

---

## 글 front matter 구조 (Lena가 글 쓸 때 사용)

```yaml
---
title: "독일 날씨가 미쳤다 — 정신병자인 이유 8가지"
description: "독일에서 2년 살며 느낀 날씨의 모든 것."
date: 2026-03-12
theme: weather
thumbnail: /assets/images/germany/german-weather/hero.jpg
tags: [날씨, 독일생활, 적응기]
lang: ko
layout: germany/post
---
```

---

## SEO — _includes/germany/seo.html 자동 생성 항목

아래 항목을 모두 자동으로 생성할 것:

```html
<!-- 기본 SEO -->
<title>{{ page.title }} | Germany Blog — lena-var4</title>
<meta name="description" content="{{ page.description }}">
<link rel="canonical" href="{{ page.url | absolute_url }}">

<!-- Open Graph -->
<meta property="og:type" content="article">
<meta property="og:title" content="{{ page.title }}">
<meta property="og:description" content="{{ page.description }}">
<meta property="og:image" content="{{ page.thumbnail | default: '/assets/images/og-default.jpg' | absolute_url }}">
<meta property="og:url" content="{{ page.url | absolute_url }}">

<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{{ page.title }}">
<meta name="twitter:description" content="{{ page.description }}">
<meta name="twitter:image" content="{{ page.thumbnail | absolute_url }}">

<!-- Article 메타 -->
<meta property="article:published_time" content="{{ page.date | date_to_xmlschema }}">
<meta property="article:author" content="Lena">

<!-- hreflang -->
<link rel="alternate" hreflang="{{ page.lang | default: 'ko' }}" href="{{ page.url | absolute_url }}">
<link rel="alternate" hreflang="x-default" href="{{ page.url | absolute_url }}">

<!-- JSON-LD -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "{{ page.title }}",
  "description": "{{ page.description }}",
  "image": "{{ page.thumbnail | absolute_url }}",
  "datePublished": "{{ page.date | date_to_xmlschema }}",
  "author": { "@type": "Person", "name": "Lena" },
  "publisher": { "@type": "Person", "name": "Lena", "url": "https://lena2027.github.io/lenaportal" }
}
</script>
```

---

## _config.yml 설정

```yaml
title: lena-var4
url: https://lena2027.github.io/lenaportal
baseurl: ""
lang: ko

collections:
  posts:
    output: true
    permalink: /germany/:year/:month/:slug/

plugins:
  - jekyll-sitemap
  - jekyll-seo-tag

defaults:
  - scope:
      path: "_posts/germany"
    values:
      layout: germany/post
      lang: ko
```

---

## 디자인 방향

- 메인 index.html의 디자인 톤 유지 (도트 패턴, 컬러풀, Fredoka One + Nunito 폰트)
- Germany 블로그는 index보다 조금 더 읽기 편한 방향으로 (본문 가독성 우선)
- 사이드바는 심플하게, 글 목록에 집중
- 테마 CSS만 교체해도 페이지 분위기가 완전히 달라지도록 설계

---

## 납품 조건

1. 모든 모듈은 독립적으로 교체 가능해야 함
2. 글 작성 시 레이아웃/CSS 코드를 건드릴 필요 없어야 함
3. 테마 추가는 CSS 파일 하나만 추가하면 되도록
4. Google SEO 완전 최적화
5. 첫 번째 글(독일 날씨)에 실제 적용한 완성본 포함
6. WRITING_GUIDE.md — Lena가 혼자 글 올릴 수 있는 가이드 포함
