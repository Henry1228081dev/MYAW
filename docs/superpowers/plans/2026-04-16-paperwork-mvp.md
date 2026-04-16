# Paperwork MVP Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a high-end, zero-friction SOW and Invoice generator for freelancers and agencies.

**Architecture:** Next.js (App Router) monolithic MVP. State managed locally via React hooks (no database needed for MVP). Focused on "Slay" aesthetics using glassmorphism and cinematic blurs.

**Tech Stack:** Next.js 14+, Tailwind CSS (High-end config), Framer Motion, Lucide-react (light stroke).

---

### Task 1: Environment & Boilerplate Setup

**Files:**
- Create: `tmp/paperwork/package.json`
- Create: `tmp/paperwork/tailwind.config.js`
- Create: `tmp/paperwork/app/layout.tsx`
- Create: `tmp/paperwork/app/page.tsx`
- Create: `tmp/paperwork/styles/globals.css`

- [ ] **Step 1: Initialize package.json**
- [ ] **Step 2: Configure Tailwind with Cinematic Presets** (Add custom blur and mesh gradient utilities).
- [ ] **Step 3: Create Global Styles** (Implement the `Ethereal Glass` background).
- [ ] **Step 4: Create Root Layout** (Set up font).

---

### Task 2: Cinematic UI Components (The "Double-Bezel" System)

**Files:**
- Create: `tmp/paperwork/components/ui/GlassCard.tsx`
- Create: `tmp/paperwork/components/ui/CinematicInput.tsx`
- Create: `tmp/paperwork/components/ui/SlayButton.tsx`

- [ ] **Step 1: Implement GlassCard** (Outer shell + Inner core nested architecture).
- [ ] **Step 2: Implement CinematicInput** (Focused on typography and subtle focus rings).
- [ ] **Step 3: Implement SlayButton** (Button-in-button trailing icon pattern).

---

### Task 3: Step 1 - The Entry (Email Capture)

**Files:**
- Modify: `tmp/paperwork/app/page.tsx`
- Create: `tmp/paperwork/components/sections/EmailEntry.tsx`

- [ ] **Step 1: Build the landing screen** (Minimal: Just a headline "Paperwork" and the email input).
- [ ] **Step 2: Add Entry Animation** (Slide up + blur fade).
- [ ] **Step 3: Handle state transition** (Move to Project Details on submit).

---

### Task 4: Step 2 - The "What We Take" Form

**Files:**
- Create: `tmp/paperwork/components/sections/ProjectForm.tsx`

- [ ] **Step 1: Implement Multi-step Bento Form** (Inputs for: User, Client, Description, Deliverables, Rate, Dates, Terms).
- [ ] **Step 2: Add progress indicator** (Minimal glass line).

---

### Task 5: Step 3 - SOW Generator (Professional Mode)

**Files:**
- Create: `tmp/paperwork/components/documents/SOWPreview.tsx`
- Create: `tmp/paperwork/lib/templates/sow.ts`

- [ ] **Step 1: Define SOW template logic**.
- [ ] **Step 2: Build the Preview UI** (Clean, authoritative typography, "Editorial Split" layout).

---

### Task 6: Step 4 - Invoice Generator (Slay Mode)

**Files:**
- Create: `tmp/paperwork/components/documents/InvoicePreview.tsx`

- [ ] **Step 1: Design the "Slay" Invoice** (Heavy blurs, high contrast, cinematic spacing, wisprflow-inspired).
- [ ] **Step 2: Add "Export" actions** (PDF print-styling).

---

### Task 7: Final Polish & Vercel Prep

**Files:**
- Create: `tmp/paperwork/vercel.json`

- [ ] **Step 1: Optimize mobile collapse** (Single-column stack).
- [ ] **Step 2: Final motion choreography check**.
