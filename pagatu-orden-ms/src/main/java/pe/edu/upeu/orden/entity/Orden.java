package pe.edu.upeu.orden.entity;

import jakarta.persistence.*;
import lombok.Data;

@Data
@Entity
@Table(name = "ordenes")
public class Orden {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private String cliente;
    private Double total;
    private String estado;
}
