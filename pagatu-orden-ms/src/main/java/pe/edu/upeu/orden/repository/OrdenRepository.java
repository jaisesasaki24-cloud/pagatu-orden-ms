package pe.edu.upeu.orden.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import pe.edu.upeu.orden.entity.Orden;

public interface OrdenRepository extends JpaRepository<Orden, Long> {
}
