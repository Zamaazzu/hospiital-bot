import { HeartPulse, Bone, Ear, Eye, Brain, Sparkles, Baby, Smile, Stethoscope } from "lucide-react";

export const DEPARTMENTS = [
  {
    id: "cardiology",
    name: "Cardiology",
    aliases: ["cardiology", "heart", "cardiac"],
    Icon: HeartPulse,
    accent: "#8A5AE5",
    tint: "#EFE7FE",
    doctors: [
      { name: "Dr. Ramesh N", hours: "09:00 AM – 01:00 PM", tokens: 24, capacity: 30 },
      { name: "Dr. Priya K", hours: "04:00 PM – 07:00 PM", tokens: 6, capacity: 30 },
    ],
  },
  {
    id: "orthopaedics",
    name: "Orthopaedics",
    aliases: ["orthopaedics", "orthopedics", "ortho", "bone", "bones", "joint"],
    Icon: Bone,
    accent: "#6A3FD6",
    tint: "#EAE1FC",
    doctors: [{ name: "Dr. Meera S", hours: "10:00 AM – 02:00 PM", tokens: 18, capacity: 30 }],
  },
  {
    id: "ent",
    name: "ENT",
    aliases: ["ent", "ear nose throat", "ear", "throat", "nose"],
    Icon: Ear,
    accent: "#B86FEA",
    tint: "#F5E9FE",
    doctors: [{ name: "Dr. Arjun P", hours: "11:00 AM – 03:00 PM", tokens: 15, capacity: 30 }],
  },
  {
    id: "ophthalmology",
    name: "Ophthalmology",
    aliases: ["ophthalmology", "opthalmology", "ophthalmologist", "eye", "eyes", "vision"],
    Icon: Eye,
    accent: "#7C3AED",
    tint: "#F0E5FD",
    doctors: [{ name: "Dr. Kavya M", hours: "02:00 PM – 06:00 PM", tokens: 20, capacity: 30 }],
  },
  {
    id: "neurology",
    name: "Neurology",
    aliases: ["neurology", "neuro", "brain", "nerve", "nerves"],
    Icon: Brain,
    accent: "#9333EA",
    tint: "#F1E4FD",
    doctors: [{ name: "Dr. Nikhil T", hours: "09:30 AM – 12:30 PM", tokens: 4, capacity: 30 }],
  },
  {
    id: "dermatology",
    name: "Dermatology",
    aliases: ["dermatology", "skin"],
    Icon: Sparkles,
    accent: "#C084FC",
    tint: "#F7ECFE",
    doctors: [{ name: "Dr. Anjali R", hours: "12:00 PM – 04:00 PM", tokens: 22, capacity: 30 }],
  },
  {
    id: "pediatrics",
    name: "Pediatrics",
    aliases: ["pediatrics", "paediatrics", "child", "children", "kids"],
    Icon: Baby,
    accent: "#A855F7",
    tint: "#F2E6FE",
    doctors: [{ name: "Dr. Sona V", hours: "09:00 AM – 01:00 PM", tokens: 27, capacity: 30 }],
  },
  {
    id: "dentistry",
    name: "Dentistry",
    aliases: ["dentistry", "dental", "teeth", "tooth"],
    Icon: Smile,
    accent: "#5B2FC2",
    tint: "#E7DEFC",
    doctors: [{ name: "Dr. Farhan I", hours: "10:00 AM – 01:00 PM", tokens: 9, capacity: 30 }],
  },
];

// Pseudo-department that bypasses the department grid entirely.
export const GENERAL_OP = {
  id: "general-op",
  name: "General OP / Casualty",
  Icon: Stethoscope,
  accent: "#8A5AE5",
  tint: "#EFE7FE",
};

export const NO_SELECTION_FLOW_IDS = ["general-op"];

export const DEPTS_PER_PAGE = 8;
export const TOTAL_PAGES = Math.ceil(DEPARTMENTS.length / DEPTS_PER_PAGE);
export const LOW_TOKEN_THRESHOLD = 10;

export const GREETING_TEXT =
  "Hi, welcome to Ananthapuri Hospital! Which doctor's appointment would you like to book, and for which department?";

export const BAR_COUNT = 44;
export const STATIC_BAR_HEIGHT = 5;
export const SILENCE_THRESHOLD = 6; // avg byte-frequency level below which we treat input as silence
