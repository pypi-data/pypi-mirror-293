// Copyright (c) QuantStack
// Distributed under the terms of the Modified BSD License.
import {
  DOMWidgetModel,
  DOMWidgetView,
  ISerializers,
} from '@jupyter-widgets/base';

import 'ol/ol.css';
import { MODULE_NAME, MODULE_VERSION } from './version';
import '../css/widget.css';
import Overlay from 'ol/Overlay';

export class BaseOverlayModel extends DOMWidgetModel {
  defaults() {
    return {
      ...super.defaults(),
      _model_name: BaseOverlayModel.model_name,
      _model_module: BaseOverlayModel.model_module,
      _model_module_version: BaseOverlayModel.model_module_version,
      _view_name: BaseOverlayModel.view_name,
      _view_module: BaseOverlayModel.view_module,
      _view_module_version: BaseOverlayModel.view_module_version,
    };
  }

  static serializers: ISerializers = {
    ...DOMWidgetModel.serializers,
  };

  static model_name = 'BaseOverlayModel';
  static model_module = MODULE_NAME;
  static model_module_version = MODULE_VERSION;
  static view_name = 'BaseOverlayView';
  static view_module = MODULE_NAME;
  static view_module_version = MODULE_VERSION;
}

export abstract class BaseOverlayView extends DOMWidgetView {
  overlay: Overlay;
  element: HTMLElement;

  render() {
    super.render();
    this.createElement();
    this.createOverlay();
    this.model_events();
  }
  abstract createElement(): void;

  createOverlay() {
    const position = this.model.get('position');
    this.overlay = new Overlay({
      position: position,
      element: this.element,
    });
    return this.overlay;
  }

  model_events() {
    this.listenTo(this.model, 'change:position', this.updatePosition);
  }

  updatePosition() {
    const position = this.model.get('position');
    this.overlay.setPosition(position);
  }
}
