import Image from "next/image";

type FigureCardProps = {
  title: string;
  description: string;
  src: string;
  alt: string;
};

export function FigureCard({ title, description, src, alt }: FigureCardProps) {
  return (
    <article className="card visual-card">
      <div>
        <h3>{title}</h3>
        <p className="muted">{description}</p>
      </div>
      <Image src={src} alt={alt} width={1200} height={800} unoptimized />
    </article>
  );
}
